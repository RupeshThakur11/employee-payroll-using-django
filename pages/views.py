from django.http import HttpResponseRedirect
from django.shortcuts import render
from employee.models import Office, Employee, SalaryRecord


def home_view(request, *args, **kwargs):
    data = get_login(request)
    if data['type'] == "employee":
        queryset = SalaryRecord.objects.filter(emp_id=data['id'])
        return render(request, "home.html", {"queryset": queryset})
    else:
        return HttpResponseRedirect('/')


def office_home_view(request, *args, **kwargs):
    data = get_login(request)
    if data['type'] == 'office':
        queryset = Employee.objects.all()
        if request.method == 'POST':
            print(request.POST.items())
            base_salary = request.POST.get('base_salary')
            hra = request.POST.get('hra')
            da = request.POST.get('da')
            ta = request.POST.get('ta')
            pf = request.POST.get('pf')
            working_days = request.POST.get('working_days')
            leaves = request.POST.get('leaves')
            employee = Employee.objects.get(id=request.POST.get("employee"))
            record = SalaryRecord(base_salary=base_salary, hra=hra, da=da, ta=ta, pf=pf, emp_id=employee, working_days=working_days, leaves=leaves)
            record.save()
            send_email(employee.email, "Salary", "Your Salary Has Been Credited. You can check details by logging into your account.")
            return HttpResponseRedirect('/office/home/?saved=True')

        return render(request, "office-home.html", {"queryset": queryset})
    else:
        return HttpResponseRedirect('/office/')


def office_view_records(request, *args, **kwargs):
    data = get_login(request)
    if data['type'] == "office":
        queryset = SalaryRecord.objects.all()
        return render(request, "view-records.html", {"queryset": queryset})
    else:
        return HttpResponseRedirect('/office/')


def login(request, *args, **kwargs):
    data = get_login(request)
    if len(data) == 0:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            type = request.POST.get('type')
            user = authenticate(email, password, type)
            if user is not None:
                request.session['type'] = type
                request.session['id'] = user.id
                print("Inside not none")
                if type == 'office':
                    return HttpResponseRedirect('/office/home/')
                else:
                    return HttpResponseRedirect('/home/')
            else:
                if type == 'office':
                    return HttpResponseRedirect('/office/?failed=True')
                else:
                    return HttpResponseRedirect('/?failed=True')

        else:
            context = {
                "type": kwargs['type']
            }
            return render(request, "login.html", context)

    else:
        if data['type'] == 'office':
            return HttpResponseRedirect('/office/home/')
        else:
            return HttpResponseRedirect('/home/')


def authenticate(email, password, type):
    if type == "office":
        data = Office.objects.filter(email=email, password=password)
        if len(data) == 0:
            return None
        else:
            return Office.objects.get(email=email, password=password)
    elif type == "employee":
        data = Employee.objects.filter(email=email, password=password)
        if len(data) == 0:
            return None
        else:
            return Employee.objects.get(email=email, password=password)


def get_login(request):
    data = {}
    if request.session.has_key('type'):
        data['type'] = request.session['type']

    if request.session.has_key('id'):
        data['id'] = request.session['id']
    print(data)
    return data


def logout(request):
    data = get_login(request)
    if len(data) == 2:
        del request.session['id']
        del request.session['type']
        return HttpResponseRedirect('/')


def send_email(recipient, subject, body):
    import smtplib
    user = "dhivarshiva96@gmail.com"
    pwd = "Dish@nk@1"
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print("failed to send mail")
