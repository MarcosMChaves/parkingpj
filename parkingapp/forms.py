from django import forms
from django.forms import ModelForm
from .models import Área, Estacionamento, Estadia, Fabricante, Modelo, Porte, Vaga, Veículo

class ÁreaForm(ModelForm):
	class Meta():
		model = Área
		fields = ['nome_área', 'fk_estacionamento',]
		labels = {
			'nome_área':'Área',
			'fk_estacionamento':'Estacionamento',
		}
		widgets = {
				'nome_área': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
				'fk_estacionamento': forms.Select(attrs={'class':'form-select'}),				
			}

class ÁreaFormRO(ModelForm):
	class Meta():
		model = Área
		fields = ['nome_área', 'fk_estacionamento',]
		labels = {
			'nome_área':'Área',
			'fk_estacionamento':'Estacionamento',
		}
		widgets = {
				'nome_área': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome', 'readonly':'readonly'}),
				'fk_estacionamento': forms.Select(attrs={'class':'form-select', 'disabled':'disabled'}),				
			}

class EstacionamentoForm(ModelForm):
	class Meta():
		model = Estacionamento
		fields = ['razão_social_estacionamento', 
					'nome_fantasia_estacionamento',
					'cnpj_estacionamento', 
					'gratuidade_estacionamento', 
					'fração_estacionamento']
		labels = {
			'razão_social_estacionamento':'Razão Social',
			'nome_fantasia_estacionamento':'Nome Fantasia',
			'cnpj_estacionamento':'CNPJ',
			'gratuidade_estacionamento':'Período Gratuidade',
			'fração_estacionamento':'Fração Arredondamento',
		}
		widgets = {
				'razão_social_estacionamento': forms.TextInput(attrs={'class':'form-control','placeholder':'Razão Social'}),
				'nome_fantasia_estacionamento': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome Fantasia'}),
				'cnpj_estacionamento': forms.TextInput(attrs={'class':'form-control','placeholder':'CNPJ'}),
				'gratuidade_estacionamento': forms.TimeInput(attrs={'class':'form-control','placeholder':'Período Gratuidade'}),
				'fração_estacionamento': forms.TimeInput(attrs={'class':'form-control','placeholder':'Fração Arredondamento'}),
			}

class FabricanteForm(ModelForm):
	class Meta():
		model = Fabricante
		fields = ['nome_fantasia_fabricante']
		labels = {
			'nome_fantasia_fabricante':'Fabricante',
		}
		widgets = {
				'nome_fantasia_fabricante': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
			}

class FabricanteFormRO(ModelForm):
	class Meta():
		model = Fabricante
		fields = ['nome_fantasia_fabricante']
		labels = {
			'nome_fantasia_fabricante':'Fabricante',
		}
		widgets = {
				'nome_fantasia_fabricante': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome', 'readonly':'readonly'}),
			}

class ModeloForm(ModelForm):
	class Meta():
		model = Modelo
		fields = ['nome_modelo', 'fk_fabricante', 'fk_porte',]
		labels = {
			'nome_modelo':'Modelo',
			'fk_fabricante':'Fabricante',
			'fk_porte':'Porte',
		}
		widgets = {
				'nome_modelo': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
				'fk_fabricante': forms.Select(attrs={'class':'form-select'}),				
				'fk_porte': forms.Select(attrs={'class':'form-select'}),				
			}

class ModeloFormRO(ModelForm):
	class Meta():
		model = Modelo
		fields = ['nome_modelo', 'fk_fabricante', 'fk_porte',]
		labels = {
			'nome_modelo':'Modelo',
			'fk_fabricante':'Fabricante',
			'fk_porte':'Porte',
		}
		widgets = {
				'nome_modelo': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome', 'readonly':'readonly'}),
				'fk_fabricante': forms.Select(attrs={'class':'form-select', 'disabled':'disabled'}),				
				'fk_porte': forms.Select(attrs={'class':'form-select', 'disabled':'disabled'}),				
			}

class PorteForm(ModelForm):
	class Meta():
		model = Porte
		fields = ['nome_porte', 'sigla_porte', 'valor_hora']
		labels = {
			'nome_porte':'Porte',
			'sigla_porte':'Sigla Porte',
			'valor_hora':'Valor Hora',
		}
		widgets = {
				'nome_porte': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
				'sigla_porte': forms.TextInput(attrs={'class':'form-control','placeholder':'Sigla'}),
				'valor_hora': forms.NumberInput(attrs={'class':'form-control','placeholder':'Valor Hora'}),
			}

class PorteFormRO(ModelForm):
	class Meta():
		model = Porte
		fields = ['nome_porte', 'sigla_porte', 'valor_hora']
		labels = {
			'nome_porte':'Porte',
			'sigla_porte':'Sigla Porte',
			'valor_hora':'Valor Hora',
		}
		widgets = {
				'nome_porte': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome', 'readonly':'readonly'}),
				'sigla_porte': forms.TextInput(attrs={'class':'form-control','placeholder':'Sigla', 'readonly':'readonly'}),
				'valor_hora': forms.NumberInput(attrs={'class':'form-control','placeholder':'Valor Hora', 'readonly':'readonly'}),
			}

class VagaForm(ModelForm):
	class Meta():
		model = Vaga
		fields = ['nome_vaga', 'fk_área',]
		labels = {
			'nome_vaga':'Vaga',
			'fk_área':'Área',
		}
		widgets = {
				'nome_vaga': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome'}),
				'fk_área': forms.Select(attrs={'class':'form-select'}),				
			}

class VagaFormRO(ModelForm):
	class Meta():
		model = Vaga
		fields = ['nome_vaga', 'fk_área',]
		labels = {
			'nome_vaga':'Vaga',
			'fk_área':'Área',
		}
		widgets = {
				'nome_vaga': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome', 'readonly':'readonly'}),
				'fk_área': forms.Select(attrs={'class':'form-select', 'disabled':'disabled'}),				
			}

class VeículoForm(ModelForm):
	class Meta():
		model = Veículo
		fields = ['chapa_veículo', 'fk_modelo',]
		labels = {
			'chapa_veículo':'Placa',
			'fk_modelo':'Modelo',
		}
		widgets = {
				'chapa_veículo': forms.TextInput(attrs={'class':'form-control','placeholder':'Placa'}),
				'fk_modelo': forms.Select(attrs={'class':'form-select'}),				
			}

class VeículoFormRO(ModelForm):
	class Meta():
		model = Veículo
		fields = ['chapa_veículo', 'fk_modelo',]
		labels = {
			'chapa_veículo':'Placa',
			'fk_modelo':'Modelo',
		}
		widgets = {
				'chapa_veículo': forms.TextInput(attrs={'class':'form-control','placeholder':'Placa', 'readonly':'readonly'}),
				'fk_modelo': forms.Select(attrs={'class':'form-select', 'disabled':'disabled'}),				
			}