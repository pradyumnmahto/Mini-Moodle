def handle_uploaded_file(f): 
    """Function to handle the uploaded file

    Args:
        f (file): File to be handled
    """     
    with open('media/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():  
            destination.write(chunk)  