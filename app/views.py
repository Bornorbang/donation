from django.shortcuts import render, redirect, get_object_or_404
from app.models import Project, Donate
from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm, DonationForm
from django.core.paginator import Paginator
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
import stripe


# Create your views here.


def index(request):
    projects = Project.objects.filter(id__in=[26,2,3])

    context ={
        "projects": projects
    }
    return render(request, 'index.html', context)


def aboutus(request):
    context = {}

    return render(request,'aboutus.html', context)

def bankaccounts(request):

    return render(request, 'bankaccounts.html')

def project(request):
    projects = Project.objects.all()

    context ={
        "projects": projects
    }

    return render(request, 'projects.html', context)


def donatewealthy(request):
    projects = Project.objects.filter(category__name='wealthy')

    # Create a paginator with 3 projects per page
    paginator = Paginator(projects, 6) 

    # Get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        "projects": projects,
        "page_obj": page_obj

    }

    return render(request, 'donatewealthy.html', context)

def raisetoraise(request):
    projects = Project.objects.filter(category__name="raise")

    context = {
        "projects": projects
    }

    return render(request, 'raisetoraise.html', context)

def zakat(request):

    context ={}

    return render(request, 'zakat.html', context)

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your landing page
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your landing page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def PaymentSuccess(request, project_id, donate_id):
    project = Project.objects.get(id=project_id)
    donate = get_object_or_404(Donate, id=donate_id)

    return render(request, 'payment_success.html', {'project': project, 'donate': donate})


def PaymentFailure(request, project_id, donate_id):
    project = get_object_or_404(Project, id=project_id)
    donate = get_object_or_404(Donate, id=donate_id)

    return render(request, 'payment_failure.html', {'project': project, 'donate': donate})

def donation_history(request):
    context = {}

    return render(request, 'donation_history.html', context)

def project_detail(request, project_id):
    projects = Project.objects.get(id=project_id)

    return render(request, 'project_detail.html', {'project': projects})


def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donate = form.save(commit=False)
            donate.project = project
            donate.save()
            # Redirect with both project_id and donate_id
            return redirect('checkout', project_id=project.id, donate_id=donate.id)
    else:
        form = DonationForm()
    
    return render(request, 'donate_modal.html', {'form': form, 'project': project})


def checkout(request, project_id, donate_id):
    project = get_object_or_404(Project, id=project_id)
    donate = get_object_or_404(Donate, id=donate_id)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'currency_code': 'USD',
        'amount': donate.amount,
        'item_name': f'{project.title} - Donation',
        'invoice': str(uuid.uuid4()),
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment_success", kwargs={"project_id": project.id, "donate_id": donate.id})}',
        'cancel_url': f'http://{host}{reverse("payment_failure", kwargs={"project_id": project.id, "donate_id": donate.id})}',

    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        "project": project,
        "donate": donate,
        'paypal': paypal_payment
    }
    return render(request, 'checkout.html', context)


def stripe_checkout(request, project_id, donate_id):
    project = get_object_or_404(Project, id=project_id)
    donate = get_object_or_404(Donate, id=donate_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"{project.title} - Donation",
                },
                'unit_amount': int(donate.amount * 100),  # Convert to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success', kwargs={"project_id": project.id, "donate_id": donate.id})),
        cancel_url=request.build_absolute_uri(reverse('payment_failure', kwargs={"project_id": project.id, "donate_id": donate.id})),
    )

    return redirect(session.url, code=303)