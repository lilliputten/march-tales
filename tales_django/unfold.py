# from app.models import MyModel

def dashboard_callback(request, context):
    context.update({
        "variable": "Test", # MyModel.objects.some_results()
    })

    return context
