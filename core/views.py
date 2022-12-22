from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Tarefa
from core.resources import TarefaResource
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User
import zipfile
from io import BytesIO
import tablib
from import_export import resources
import xlrd

# Create your views here.
@login_required(login_url="/login/")
def lista_tarefas(request):
    usuario = request.user
    tarefa = Tarefa.objects.filter(usuario=usuario)
    return render(request, "lista_tarefas.html", {"tarefas": tarefa})


def login_user(request):
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def submit_login(request):
    if request.POST:
        username = request.POST.get("user")
        password = request.POST.get("password")
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("/")
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect("/")


def register_user(request):
    if request.POST:
        username = request.POST.get("user")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password == password2:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect("/")
        else:
            messages.error(request, "Senhas não conferem")
    return render(request, "register.html")


@login_required(login_url="/login/")
def tarefa(request):
    id_tarefa = request.GET.get("id")
    dados = {}
    if id_tarefa:
        dados["tarefa"] = Tarefa.objects.get(id=id_tarefa)

    return render(request, "tarefa.html", dados)


@login_required(login_url="/login/")
def submit_tarefa(request):
    if request.POST:
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        data_expiracao = request.POST.get("date")
        usuario = request.user
        id_tarefa = request.POST.get("id_tarefa")
        if id_tarefa:
            print(id_tarefa)
            Tarefa.objects.filter(id=id_tarefa).update(
                titulo=titulo, descricao=descricao, data_expiracao=data_expiracao
            )
        else:
            Tarefa.objects.create(
                titulo=titulo,
                descricao=descricao,
                usuario=usuario,
                data_expiracao=data_expiracao,
            )

        return redirect("/")
    return redirect("/")


@login_required(login_url="/login/")
def delete_tarefa(request, id_tarefa):
    usuario = request.user
    try:
        tarefa = Tarefa.objects.get(id=id_tarefa)
    except Tarefa.DoesNotExist:
        raise Http404()

    if tarefa.usuario == usuario:
        tarefa.delete()
    else:
        raise Http404()
    return redirect("/")


@login_required(login_url="/login/")
def about_us(request):
    return render(request, "about_us.html")


@login_required(login_url="/login/")
def search_tarefa(request):
    if request.POST:
        search = request.POST.get("search")
        tarefas = Tarefa.objects.filter(titulo__icontains=search, usuario=request.user)
        return render(request, "lista_tarefas.html", {"tarefas": tarefas})
    return redirect("/")


@login_required(login_url="/login/")
def export_tarefas(request):
    if request.POST:
        tarefas = Tarefa.objects.filter(usuario=request.user)
        tarefa_resource = TarefaResource()
        dataset = tarefa_resource.export(tarefas)
        option = request.POST.get("option")

        print("POST", option)

        if option == "xls":
            response = HttpResponse(
                dataset.xls, content_type="application/vnd.ms-excel"
            )
            response[
                "Content-Disposition"
            ] = f"attachment; filename=tarefas_{request.user}.xls"
            return response
        elif option == "csv":
            response = HttpResponse(dataset.csv, content_type="text/csv")
            response[
                "Content-Disposition"
            ] = f"attachment; filename=tarefas_{request.user}.csv"
            return response
        elif option == "json":
            response = HttpResponse(dataset.json, content_type="text/json")
            file = BytesIO()
            with zipfile.ZipFile(file, "w") as zip:
                zip.writestr(
                    f"tarefas_{request.user}.json", response.content.decode("utf-8")
                )
                zip.close()
            response = HttpResponse(
                file.getvalue(), content_type="application/x-zip-content"
            )
            file.close()
            response[
                "Content-Disposition"
            ] = f"attachment; filename=tarefas_{request.user}.zip"
            return response
        else:
            return render(request, "export.html")
    return render(request, "export.html")


@login_required(login_url="/login/")
def import_tarefas(request):
    if request.POST:
        try:
            file = request.FILES["file"]
            if file is None:
                raise Exception("Arquivo não encontrado", file_name)
        except Exception as e:
            messages.error(request, e, extra_tags="danger")
            return render(request, "import.html")
        
        print(file)
        if file.name.endswith(".xls") or file.name.endswith(".xlsx"):
            try:
                print("xls")
                data = tablib.import_set(file.read(), format="xls")
                tarefa_resource = resources.modelresource_factory(model=Tarefa)()
                dataset = tarefa_resource.import_data(data, dry_run=True)
                if not dataset.has_errors():
                    tarefa_resource.import_data(data, dry_run=False)
                    messages.success(request, "Tarefas importadas com sucesso", extra_tags="success")
                    return render(request, "import.html")
                else:
                    messages.error(request, "Erro na importação", extra_tags="danger")
                    return render(request, "import.html")
            except Exception as e:
                messages.error(request, e, extra_tags="danger")
                return render(request, "import.html")
        elif file.name.endswith(".csv"):
            try:
                print("csv")
                data = tablib.import_set(file.read().decode("utf-8"), format="csv")
                tarefa_resource = resources.modelresource_factory(model=Tarefa)()
                dataset = tarefa_resource.import_data(data, dry_run=True)
                if not dataset.has_errors():
                    tarefa_resource.import_data(data, dry_run=False)
                    messages.success(request, "Tarefas importadas com sucesso", extra_tags="success")
                    return render(request, "import.html")
                else:
                    messages.error(request, "Erro na importação", extra_tags="danger")
                    return render(request, "import.html")
            except Exception as e:
                messages.error(request, "Erro na importação", extra_tags="danger")
                return render(request, "import.html")
        elif file.name.endswith(".json"):
            try:
                print("json")
                data = tablib.import_set(file.read().decode("utf-8"), format="json")
                tarefa_resource = resources.modelresource_factory(model=Tarefa)()
                dataset = tarefa_resource.import_data(data, dry_run=True)
                if not dataset.has_errors():
                    tarefa_resource.import_data(data, dry_run=False)
                    messages.success(request, "Tarefas importadas com sucesso", extra_tags="success")
                    return render(request, "import.html")
                else:
                    messages.error(request, "Erro na importação", extra_tags="danger")
                    return render(request, "import.html")
            except Exception as e:
                messages.error(request, e, extra_tags="danger")
                return render(request, "import.html")
    return render(request, "import.html")