from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db.models import Count, Sum
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import time
from django.utils import timezone
import pytz
import random
import math
from .models import Área, Cliente, Estacionamento, Estadia, Fabricante, Modelo, Ocupação, Ocupada, Porte, Vaga, Veículo, VeículoDisponível
from .forms import ÁreaForm, ÁreaFormRO, EstacionamentoForm, FabricanteForm, FabricanteFormRO, ModeloForm, ModeloFormRO, PorteForm, PorteFormRO, VagaForm, VagaFormRO, VeículoForm, VeículoFormRO

from .config import *

# Create your views here.

from datetime import datetime

def home(request):
	agora = datetime.now()
	current_year = agora.year

	return render(request, 'parkingapp/home.html', {
		'current_year': current_year,
		})

#ÁREA
def área_listar(request):
	agora = datetime.now()
	current_year = agora.year

	áreas = Área.objects.all().order_by('nome_área')

	p = Paginator(áreas, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/área_listar.html', {
				'current_year': current_year,
				'pages':pages})	

def área_inserir(request):
	if request.method == 'POST':
		form = ÁreaForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_área'].value()
			
			messages.success(request, (f'Área "{nome}" salva com sucesso!'))
			return HttpResponseRedirect('/áreas')
	else:
		form = ÁreaForm()

	return render(request, 'parkingapp/área_inserir.html',{'form': form})

def área_editar(request, área_id):
	área = Área.objects.get(pk=área_id)
	form = ÁreaForm(request.POST or None, instance=área)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_área'].value()
		
			messages.success(request, (f'Área "{nome}" atualizada com sucesso!'))
			return HttpResponseRedirect('/áreas')
	
	return render(request, 'parkingapp/área_editar.html',{'form': form})

def área_excluir(request, área_id):
	área = Área.objects.get(pk=área_id)
	form = ÁreaFormRO(request.POST or None, instance=área)

	if request.method == 'POST':
		vaga = Vaga.objects.all().filter(fk_área=área_id)
		nome = form['nome_área'].value()
		if not vaga:
			área.delete()
			messages.success(request, (f'Área "{nome}" excluída com sucesso!'))
		else:
			messages.warning(request, (f'Área "{nome}" já possui movimento. Não pode ser excluído...'))
		return HttpResponseRedirect('/áreas')
	
	return render(request, 'parkingapp/área_excluir.html',{'form': form})

#ESTACIONAMENTO
def estacionamento_listar(request):
	agora = datetime.now()
	de_agora = agora.date()
	current_year = agora.year

	de_saída = str(de_agora)
	até_saída = str(de_agora + timedelta(days=1))

	estacionamento = Estacionamento.objects.all().order_by('razão_social_estacionamento')
	total_receita = Estadia.objects.all().filter(data_hora_saída__range=(de_saída,até_saída)).aggregate(Sum('valor_estadia'))

	p = Paginator(estacionamento, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/estacionamento_listar.html', {
				'current_year': current_year,
				'total_receita':total_receita,
				'pages':pages})	

def estacionamento_inserir(request):
	if request.method == 'POST':
		form = EstacionamentoForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_fantasia_estacionamento'].value()
			
			messages.success(request, (f'Estacionamento "{nome}" salvo com sucesso!'))
			return HttpResponseRedirect('/estacionamentos')
	else:
		form = EstacionamentoForm()

	return render(request, 'parkingapp/estacionamento_inserir.html',{'form': form})

def estacionamento_editar(request, estacionamento_id):
	estacionamento = Estacionamento.objects.get(pk=estacionamento_id)
	form = EstacionamentoForm(request.POST or None, instance=estacionamento)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_fantasia_estacionamento'].value()
		
			messages.success(request, (f'Estacionamento "{nome}" atualizado com sucesso!'))
			return HttpResponseRedirect('/estacionamentos')
	
	return render(request, 'parkingapp/estacionamento_editar.html',{'form': form})

#ESTADIA
def estadia_listar(request):
	agora = datetime.now()
	current_year = agora.year

	vagas = Vaga.objects.all().order_by('fk_área', 'nome_vaga') #TODAS AS vagas
	livres = Ocupação.objects.all()
	veículos = VeículoDisponível.objects.all().order_by('chapa_veículo')
	modelos = Modelo.objects.all().order_by('nome_modelo')

#APENAS VAGAS LIVRES!
	livre = Ocupação.objects.all().filter(data_hora_entrada__isnull=True)

#GERAR CLIENTE
	estacionamento = Estacionamento.objects.all().order_by('id_estacionamento')

	if estacionamento:
		novo_cliente = Cliente()
		placa, modelo = novo_cliente.gerar_cliente(veículos, modelos)
	else:
		placa = modelo = ''

	return render(request, 'parkingapp/estadia_listar.html', {
				'current_year': current_year,
				'agora':agora,
				'vagas':vagas,
				'livres':livres,
				'livre': livre,
				'limite':AVISO_LIMITE,
				'DÍGITOS':DÍGITOS,
				'placa':placa,
				'modelo':modelo,
				'veículos':veículos})	

def estadia_entrada(request):
	agora = timezone.now()
	current_year = agora.year

	if request.method == 'POST':
		chapa = request.POST.get("chapa", None)
		veículos = Veículo.objects.get(chapa_veículo=chapa)			

		veículo, vaga = inserir_estadia(veículos)
		if veículo:
			messages.success(request, (f"Entrada de '{ veículo }' na vaga '{ vaga }' realizada com sucesso!"))
		else:
			messages.warning(request, (f"Entrada no estacionamento requer um veículo!"))

	vagas = Vaga.objects.all().order_by('fk_área', 'nome_vaga') #TODAS AS vagas
	livres = Ocupação.objects.all()
	veículos = VeículoDisponível.objects.all().order_by('chapa_veículo')
	modelos = Modelo.objects.all().order_by('nome_modelo')

#APENAS VAGAS LIVRES!
	livre = Ocupação.objects.all().filter(data_hora_entrada__isnull=True)
	messages.warning(request, (f"Não se esqueça... estacione o veículo na VAGA assinalada!"))

#GERAR CLIENTE
	estacionamento = Estacionamento.objects.all().order_by('id_estacionamento')

	if estacionamento:
		novo_cliente = Cliente()
		placa, modelo = novo_cliente.gerar_cliente(veículos, modelos)
	else:
		placa = modelo = ''

	return render(request, 'parkingapp/estadia_listar.html', {
				'current_year': current_year,
				'agora':agora,
				'vagas':vagas,
				'livres':livres,
				'livre': livre,
				'limite':AVISO_LIMITE,
				'DÍGITOS':DÍGITOS,
				'placa':placa,
				'modelo':modelo,
				'veículos':veículos})	

def inserir_estadia(veículo):
	agora = timezone.now()
	chapa = veículo.id_veículo
	if chapa > 0:
		livre = Ocupação.objects.all().filter(data_hora_entrada__isnull=True)
		escolha = random.choice(livre)			
		veículo = Veículo.objects.get(pk=chapa)
		vaga = Vaga.objects.get(pk=escolha.id_vaga)
		estadia = Estadia.objects.create(fk_vaga=vaga, fk_veículo=veículo, data_hora_entrada=agora, valor_estadia=0)
		return veículo, vaga
	else:
		return False, False

def estadia_saída(request, estadia_id):
	agora = timezone.now()
	current_year = agora.year

	estadia = get_object_or_404(Estadia, pk=estadia_id)
	chapa_veículo = estadia.fk_veículo.chapa_veículo
	estacionamento = Estacionamento.objects.get(pk=1)	#SÓ PODE EXISTIR UM ESTACIONAMENTO

	#ATUALIZA SAÍDA
	estadia.data_hora_saída = agora
	
	#CALCULA DURAÇÃO DA ESTADIA
	utc=pytz.UTC
	date_in = estadia.data_hora_entrada
	date_out = estadia.data_hora_saída
	duração = date_out - date_in	 
	
	#CALCULA VALOR DA ESTADIA
	valor = estadia.fk_veículo.fk_modelo.fk_porte.valor_hora
	duração_minutos = duração.total_seconds() / 60
	d_minutos = timedelta(0,minutes=duração_minutos,seconds=0)
	d_minutos = (datetime.min + d_minutos).time()
	gratuidade = estacionamento.gratuidade_estacionamento

	if d_minutos <= estacionamento.gratuidade_estacionamento:	#APLICA GRATUIDADE
		total = 0
		gratuidade = gratuidade.strftime("%H:%M")
		messages.success(request, (f"Paradinha GRÁTIS (menos de {gratuidade} min.)!"))
	else:
		fração_t = estacionamento.fração_estacionamento
		fração = fração_t.minute
		duração_ajustada = math.ceil(duração_minutos / fração) * fração #APLICA FRAÇÃO
		em_horas = duração_ajustada // 60
		em_minutos = ((duração_ajustada/60)-em_horas)*60

		total = duração_ajustada * float(valor) / 60
		messages.success(request, (f"Estadia ${total:.2f} ({em_horas:.0f} h {em_minutos:.0f} min. ${valor:.2f}/h)!"))

	estadia.valor_estadia = total
	estadia.save()
	messages.success(request, (f"Saída de '{ chapa_veículo }' realizada com sucesso!"))

	vagas = Vaga.objects.all().order_by('fk_área', 'nome_vaga') #TODAS AS vagas
	livres = Ocupação.objects.all()
	veículos = VeículoDisponível.objects.all().order_by('chapa_veículo')
	modelos = Modelo.objects.all().order_by('nome_modelo')

#APENAS VAGAS LIVRES!
	livre = Ocupação.objects.all().filter(data_hora_entrada__isnull=True)

#GERAR CLIENTE
	estacionamento = Estacionamento.objects.all().order_by('id_estacionamento')

	if estacionamento:
		novo_cliente = Cliente()
		placa, modelo = novo_cliente.gerar_cliente(veículos, modelos)
	else:
		placa = modelo = ''

	return render(request, 'parkingapp/estadia_listar.html', {
				'current_year': current_year,
				'agora':agora,
				'vagas':vagas,
				'livres':livres,
				'livre': livre,
				'limite':AVISO_LIMITE,
				'DÍGITOS':DÍGITOS,
				'placa':placa,
				'modelo':modelo,
				'veículos':veículos})	

def receita_listar(request):
	agora = datetime.now()
	de_agora = agora.date()
	mínimo = str(agora.date() - timedelta(days=30*6))
	máximo = str(agora.date() + timedelta(days=1))
	current_year = agora.year

	de_saída = str(request.session.get('de_saída', de_agora))
	até_saída = str(request.session.get('até_saída', de_agora + timedelta(days=1)))


	if request.method == 'POST':
		if request.POST.get("filtrar"):
			de_saída = request.POST.get("de_saída", de_agora)
			até_saída = request.POST.get("até_saída", de_agora + timedelta(days=1))
			if de_saída > até_saída:
				messages.warning(request, (f"DE '{de_saída}' deve ser maior que ATÉ '{até_saída}'..."))
			else:
				request.session['de_saída'] = str(de_saída)
				request.session['até_saída'] = str(até_saída)
	else:
		de_saída = str(de_agora)
		até_saída = str(de_agora + timedelta(days=1))

	estadia = Estadia.objects.all().filter(data_hora_saída__range=(de_saída,até_saída), valor_estadia__gt=0).order_by('-data_hora_saída')
	if not estadia:
		messages.warning(request, (f"Não há dados dispóníveis no intervalo DE '{de_saída}' ATÉ '{até_saída}'..."))
	else:		
		messages.success(request, (f"Receita DE '{de_saída}' ATÉ '{até_saída}'!"))

	total_receita = Estadia.objects.all().filter(data_hora_saída__range=(de_saída,até_saída)).aggregate(Sum('valor_estadia'))

	p = Paginator(estadia, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/receita_listar.html', {
				'current_year': current_year,
				'total_receita':total_receita,
				'de_saída': de_saída,
				'até_saída': até_saída,
				'mínimo': mínimo,
				'máximo': máximo,
				'pages':pages})	

#FABRICANTE
def fabricante_listar(request):
	agora = datetime.now()
	current_year = agora.year

	fabricantes = Fabricante.objects.all().order_by('nome_fantasia_fabricante')
	qtde_modelos = Modelo.objects.values('fk_fabricante').annotate(count=Count('fk_fabricante')).order_by('fk_fabricante')

#	qtde_modelos = Modelo.objects.select_related('fabricante').all().values('id_fabricante', '').annotate(qtde=Count('id_modelo')) 

	p = Paginator(fabricantes, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/fabricante_listar.html', {
				'current_year': current_year,
				'qtde_modelos':qtde_modelos,
				'pages':pages})	

def fabricante_inserir(request):
	if request.method == 'POST':
		form = FabricanteForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_fantasia_fabricante'].value()
			
			messages.success(request, (f'Fabricante "{nome}" salvo com sucesso!'))
			return HttpResponseRedirect('/fabricantes')
	else:
		form = FabricanteForm()

	return render(request, 'parkingapp/fabricante_inserir.html',{'form': form})

def fabricante_editar(request, fabricante_id):
	fabricante = Fabricante.objects.get(pk=fabricante_id)
	form = FabricanteForm(request.POST or None, instance=fabricante)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_fantasia_fabricante'].value()
		
			messages.success(request, (f'Fabricante "{nome}" atualizado com sucesso!'))
			return HttpResponseRedirect('/fabricantes')
	
	return render(request, 'parkingapp/fabricante_editar.html',{'form': form})

def fabricante_excluir(request, fabricante_id):
	fabricante = Fabricante.objects.get(pk=fabricante_id)
	form = FabricanteFormRO(request.POST or None, instance=fabricante)

	if request.method == 'POST':
		modelo = Modelo.objects.all().filter(fk_fabricante=fabricante_id)
		nome = form['nome_fantasia_fabricante'].value()
		if not modelo:
			fabricante.delete()
			messages.success(request, (f'Fabricante "{nome}" excluído com sucesso!'))
		else:
			messages.warning(request, (f'Fabricante "{nome}" já possui movimento. Não pode ser excluído...'))
		return HttpResponseRedirect('/fabricantes')
	
	return render(request, 'parkingapp/fabricante_excluir.html',{'form': form})

#MODELO
def modelo_listar(request, fabricante_id=0):
	agora = datetime.now()
	current_year = agora.year

	if fabricante_id:
		modelos = Modelo.objects.all().filter(fk_fabricante=fabricante_id).order_by('nome_modelo')
	else:
		modelos = Modelo.objects.all().order_by('nome_modelo')

	p = Paginator(modelos, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/modelo_listar.html', {
				'current_year': current_year,
				'pages':pages})	

def modelo_inserir(request):
	if request.method == 'POST':
		form = ModeloForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_modelo'].value()
			
			messages.success(request, (f'Modelo "{nome}" salvo com sucesso!'))
			return HttpResponseRedirect('/modelos')
	else:
		form = ModeloForm()

	return render(request, 'parkingapp/modelo_inserir.html',{'form': form})

def modelo_editar(request, modelo_id):
	modelo = Modelo.objects.get(pk=modelo_id)
	form = ModeloForm(request.POST or None, instance=modelo)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_modelo'].value()
		
			messages.success(request, (f'Modelo "{nome}" atualizado com sucesso!'))
			return HttpResponseRedirect('/modelos')
	
	return render(request, 'parkingapp/modelo_editar.html',{'form': form})

def modelo_excluir(request, modelo_id):
	modelo = Modelo.objects.get(pk=modelo_id)
	form = ModeloFormRO(request.POST or None, instance=modelo)

	if request.method == 'POST':
		veículo = Veículo.objects.all().filter(fk_modelo=modelo_id)
		nome = form['nome_modelo'].value()
		if not veículo:
			modelo.delete()
			messages.success(request, (f'Modelo "{nome}" excluído com sucesso!'))
		else:
			messages.warning(request, (f'Modelo "{nome}" já possui movimento. Não pode ser excluído...'))
		return HttpResponseRedirect('/modelos')
	
	return render(request, 'parkingapp/modelo_excluir.html',{'form': form})

#PORTE
def porte_listar(request):
	agora = datetime.now()
	current_year = agora.year

	portes = Porte.objects.all().order_by('nome_porte')

	p = Paginator(portes, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/porte_listar.html', {
				'current_year': current_year,
				'pages':pages})	

def porte_inserir(request):
	if request.method == 'POST':
		form = PorteForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_porte'].value()
			
			messages.success(request, (f'Porte "{nome}" salvo com sucesso!'))
			return HttpResponseRedirect('/portes')
	else:
		form = PorteForm()

	return render(request, 'parkingapp/porte_inserir.html',{'form': form})

def porte_editar(request, porte_id):
	porte = Porte.objects.get(pk=porte_id)
	form = PorteForm(request.POST or None, instance=porte)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_porte'].value()
		
			messages.success(request, (f'Porte "{nome}" atualizado com sucesso!'))
			return HttpResponseRedirect('/portes')
	
	return render(request, 'parkingapp/porte_editar.html',{'form': form})

def porte_excluir(request, porte_id):
	porte = Porte.objects.get(pk=porte_id)
	form = PorteFormRO(request.POST or None, instance=porte)

	if request.method == 'POST':
		modelo = Modelo.objects.all().filter(fk_porte=porte_id)
		nome = form['nome_porte'].value()
		if not modelo:
			porte.delete()
			messages.success(request, (f'Porte "{nome}" excluído com sucesso!'))
		else:
			messages.warning(request, (f'Porte "{nome}" já possui movimento. Não pode ser excluído...'))
		return HttpResponseRedirect('/portes')
	
	return render(request, 'parkingapp/porte_excluir.html',{'form': form})

#VAGA
def vaga_listar(request):
	agora = datetime.now()
	current_year = agora.year

	vagas = Vaga.objects.all().order_by('fk_área', 'nome_vaga')

	p = Paginator(vagas, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/vaga_listar.html', {
				'current_year': current_year,
				'pages':pages})	

def vaga_inserir(request):
	if request.method == 'POST':
		form = VagaForm(request.POST)
		if form.is_valid():
			form.save()
			nome = form['nome_vaga'].value()
			
			messages.success(request, (f'Vaga "{nome}" salva com sucesso!'))
			return HttpResponseRedirect('/vagas')
	else:
		form = VagaForm()

	return render(request, 'parkingapp/vaga_inserir.html',{'form': form})

def vaga_editar(request, vaga_id):
	vaga = Vaga.objects.get(pk=vaga_id)
	form = VagaForm(request.POST or None, instance=vaga)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['nome_vaga'].value()
		
			messages.success(request, (f'Vaga "{nome}" atualizada com sucesso!'))
			return HttpResponseRedirect('/vagas')
	
	return render(request, 'parkingapp/vaga_editar.html',{'form': form})

def vaga_excluir(request, vaga_id):
	vaga = Vaga.objects.get(pk=vaga_id)
	form = VagaFormRO(request.POST or None, instance=vaga)

	if request.method == 'POST':
		estadia = Estadia.objects.all().filter(fk_vaga=vaga_id)
		nome = form['nome_vaga'].value()
		if not estadia:
			vaga.delete()
			messages.success(request, (f'Vaga "{nome}" excluída com sucesso!'))
		else:
			messages.warning(request, (f'Vaga "{nome}" já possui movimento. Não pode ser excluída...'))
		return HttpResponseRedirect('/vagas')
	
	return render(request, 'parkingapp/vaga_excluir.html',{'form': form})

#VEÍCULO
def veículo_listar(request):
	agora = datetime.now()
	current_year = agora.year

	estadias = Estadia.objects.all()
	veículos = Veículo.objects.all().order_by('chapa_veículo')

	p = Paginator(veículos, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/veículo_listar.html', {
				'current_year': current_year,
				'estadias': estadias,
				'pages':pages})	

def veículo_pesquisar(request):
	agora = datetime.now()
	current_year = agora.year
	filtro = request.session.get('filtro', '')

	if request.method == 'POST':
		if request.POST.get("limpar"):
			filtro = ''			
		else:
			filtro = request.POST.get("filtro", None)	
		request.session['filtro'] = filtro
	
	if filtro:
		messages.success(request, (f'Filtro aplicado com sucesso!'))			
#OK				veículos = Veículo.objects.all().filter(chapa_veículo__icontains=f'{filtro}').order_by('chapa_veículo')
#OK				veículos = Veículo.objects.all().filter(fk_modelo__nome_modelo__icontains=f'{filtro}').order_by('chapa_veículo')
#OK				veículos = Veículo.objects.all().filter(fk_modelo__fk_fabricante__nome_fantasia_fabricante__icontains=f'{filtro}').order_by('chapa_veículo')

		veículos = Veículo.objects.all().filter(Q(chapa_veículo__icontains=f'{filtro}') | Q(fk_modelo__nome_modelo__icontains=f'{filtro}') | Q(fk_modelo__fk_fabricante__nome_fantasia_fabricante__icontains=f'{filtro}')).order_by('chapa_veículo')
	else:
		if request.POST.get("filtrar"):
			messages.warning(request, (f'Não esqueça de digitar um filtro...'))			
		veículos = Veículo.objects.all().order_by('chapa_veículo')

	estadias = Estadia.objects.all()

	p = Paginator(veículos, ITENS_POR_PÁGINA)
	page = request.GET.get('page')
	pages = p.get_page(page)

	return render(request, 'parkingapp/veículo_listar.html', {
				'current_year': current_year,
				'estadias': estadias,
				'filtro': filtro,
				'pages':pages})	

def veículo_inserir(request):
	if request.method == 'POST':
		form = VeículoForm(request.POST)

		if form.is_valid():
			form.save()
			nome = form['chapa_veículo'].value()
			
			messages.success(request, (f'Veículo "{nome}" salvo com sucesso!'))
			return HttpResponseRedirect('/veículos')
	else:
		form = VeículoForm()

	return render(request, 'parkingapp/veículo_inserir.html',{'form': form})

def veículo_insert(request, placa, modelo):
	if request.method == 'POST':
		form = VeículoForm(request.POST)

		if form.is_valid():
			form.save()
			nome = form['chapa_veículo'].value()
			veículos = Veículo.objects.get(chapa_veículo=nome)			
			
			messages.success(request, (f'Veículo "{nome}" salvo com sucesso!'))

			veículo, vaga = inserir_estadia(veículos)
			if veículo:
				messages.success(request, (f"Entrada de '{ veículo }' na vaga '{ vaga }' realizada com sucesso!"))
			else:
				messages.warning(request, (f"Entrada no estacionamento requer um veículo!"))
				
			return HttpResponseRedirect('/entrada')
	else:
		form = VeículoForm()
		#ERRO
		if placa :
			modelos = Modelo.objects.get(nome_modelo=modelo)
			form = VeículoForm(initial={'chapa_veículo': placa, 'fk_modelo': modelos.id_modelo})

	return render(request, 'parkingapp/veículo_insert.html',{'form': form})

def veículo_editar(request, veículo_id):
	veículo = Veículo.objects.get(pk=veículo_id)
	form = VeículoForm(request.POST or None, instance=veículo)

	if request.method == 'POST':
		if form.is_valid():
			form.save()	
			nome = form['chapa_veículo'].value()
		
			messages.success(request, (f'Veículo "{nome}" atualizado com sucesso!'))
			return HttpResponseRedirect('/veículos')
	
	return render(request, 'parkingapp/veículo_editar.html',{'form': form})

def veículo_excluir(request, veículo_id):
	veículo = Veículo.objects.get(pk=veículo_id)
	form = VeículoFormRO(request.POST or None, instance=veículo)

	if request.method == 'POST':
		estadia = Estadia.objects.all().filter(fk_veículo=veículo_id)
		nome = form['chapa_veículo'].value()
		if not estadia:
			veículo.delete()
			
			messages.success(request, (f'Veículo "{nome}" excluído com sucesso!'))
		else:
			messages.warning(request, (f'Veículo "{nome}" já possui movimento. Não pode ser excluído...'))
		return HttpResponseRedirect('/veículos')

	return render(request, 'parkingapp/veículo_excluir.html',{'form': form})

#AUTHENTICATION
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, (f'Usuário "{user}" conectado com sucesso!'))
			if user.is_staff:
				return redirect('home')
			else:
				return redirect('estadia_listar')
		else:
			messages.error(request, ('Erro no login... verifique usuário/senha.'))
			return redirect('user_login')
	else:
		return render(request, 'parkingapp/user_login.html', {})

def user_logout(request):
	logout(request)
	messages.success(request, ('Usuário desconectado com sucesso!'))
	return redirect('home')
