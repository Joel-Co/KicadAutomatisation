import threading
from django.utils import timezone
import os
from urllib.parse import urlencode
from django.http import HttpResponse
import pcbnew
from celery import shared_task

from django.shortcuts import get_object_or_404, redirect
from myapp.models import Drc_error, ModelList, PanelFile, ResultFile
from django.core.files import File
from myapp.myscripts.update_panel_file import update_panel_file
from myapp.myscripts.panelize_pcb import panelize_pcb




@shared_task
def panelize_pcb_task(selected_files, maxHeight, maxWidth, spacing, fit_mode, request, output_file):

    user = request.user
    POST = request.POST

    request.session['progress'] = 10
    request.session.save()

    # Convert the selected file IDs into ResultFile objects
    result_files = ResultFile.objects.filter(id__in=selected_files)

    amounts_list = [0] * (int(max(selected_files)) + 1)
    print(amounts_list)

    # Update the result_files list based on the selected amount
    updated_result_files = []
    for file_id, file in zip(selected_files, result_files):
        file.locked = True
        file.save()
        
        amount = int(POST.get(f'amount_{file_id}', 1))
        print(file_id, amount)
        amounts_list[int(file_id)] = amount

        updated_result_files.extend([file] * amount)

    output_file = "output_panel.kicad_pcb"

    request.session['progress'] = 11
    request.session.save()

    ShovedIn = panelize_pcb(updated_result_files, pcbnew.FromMM(spacing), fit_mode, output_file, (pcbnew.FromMM(maxWidth), pcbnew.FromMM(maxHeight)))

    request.session['progress'] = 80
    request.session.save()

    response = HttpResponse(content_type='application/kicad_pcb')
    response['Content-Disposition'] = 'attachment; filename="output_panel.kicad_pcb"'

    # Open the zip file in binary mode and write its content to the response
    output_file_data = open(output_file, 'rb')
    #response.write(output_file.read())

    # Delete the temporary zip file
    os.remove(output_file)

    drc_errors = []

    for result_file in result_files:
        for error in result_file.Errors.errors_names:
            if not error in drc_errors:
                drc_errors.append(error)
    print(drc_errors)

    drc_error_object = Drc_error.objects.create()
    if drc_errors: drc_error_object.errors_names = drc_errors
    drc_error_object.save()

    amounts = ModelList.objects.create()
    amounts.values = amounts_list
    amounts.save()

    myPanel = PanelFile.objects.create(                
            user=user,
            filename= f"{','.join(ShovedIn):.20} {timezone.now()}",
            panel_file=File(output_file_data),
            kicad_pcb=File(output_file_data),
            description="A panel composed of " + f"{','.join(ShovedIn):.40}",
            uploaded_at = timezone.now(),
            Errors = drc_error_object,
            amounts = amounts
            )


    for result_file in result_files:
        myPanel.result_files.add(result_file.id)
    
    query_params = urlencode({
        'selected_files': selected_files,
        'board_height': f"{maxHeight}",
        'board_width': f"{maxWidth}",
        'myPanel': myPanel.id,
        'filenames': [get_object_or_404(ResultFile, id=file_id).filename for file_id in selected_files],
        'spacing': spacing, 
        'fit_mode': fit_mode
    })
    

    request.session['progress'] = 85
    request.session.save()

    threading.Thread(target=update_panel_file, args=(myPanel,)).start()

    request.session['progress'] = 100
    request.session['redirect_url'] = f"file-explorer/?{query_params}"
    request.session.save()

    #response.content['redirect_url': f"file-explorer/?{query_params}"]
    return redirect(f"file-explorer/?{query_params}")