from django.shortcuts import render

def main_page(request):
    print("GOING THROUGH THE VIEW")
    return render(request, 'chat/welcome.html')