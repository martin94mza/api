import datetime

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    JSONField,
    SerializerMethodField
    )

from rest_framework.validators import ValidationError

from aplicaciones.base.models import (
    CentroDonacion,
    Direccion,
    Donacion,
    EstadoDonacion,
    Evento,
    HistoricoEstadoDonacion,
    Localidad,
    LugarDonacion,
    RegistroDonacion
    )

from aplicaciones.direcciones.api.serializers import (
    LugarDonacionSerializer
    )

ESTADO_VERIFICADA = 'verificada'


def obtener_lugar_donacion(datos_ingresados):

    '''
    Método para determinar el LugarDonacion a asociar con la Donacion según la
    opción ingresada por el donante al momento de crear o actualizar la donación.
    '''

    centro = datos_ingresados.get('centroDonacion', None)
    evento = datos_ingresados.get('evento', None)
    direccion = datos_ingresados.get('direccion', None)

    lugar_donacion = None
    # Donación realizada en un centro de donación.
    if centro is not None:
        centro = CentroDonacion.objects.get(id=centro)
        lugar_donacion = centro.lugarDonacion
    # Donación realizada en un evento.
    elif evento is not None:
        eventoDonacion = Evento.objects.get(id=evento)
        lugar_donacion = eventoDonacion.lugarEvento.last().lugarDonacion
    # Donación realizada en una dirección en particular.
    elif direccion is not None:
        localidad = Localidad.objects.get(id=int(direccion['localidad']))

        nuevaDireccion = Direccion.objects.create(
            localidad=localidad,
            calle=direccion['calle'],
            numero=direccion['numero']
            )

        lugar_donacion = LugarDonacion.objects.create(
            direccion=nuevaDireccion
            )
    # Si no ingresó ninguna opción de lugar.
    else:
        raise ValidationError('Debes ingresar un lugar donde realizaste tu donación.')

    return lugar_donacion


def create_update_destroy_donacion_serializer(usuario):
    class DonacionCreateUpdateDestroySerializer(ModelSerializer):
        centroDonacion = CharField(write_only=True, required=False)
        evento = CharField(write_only=True, required=False)
        direccion = JSONField(binary=True, write_only=True, required=False)

        class Meta:
            model = Donacion
            fields = [
                'fechaHora',
                'foto',
                'descripcion',
                'centroDonacion',
                'evento',
                'estado',
                'direccion'
            ]

        def validate_fechaHora(self, value):
            if value > datetime.datetime.now():
                raise ValidationError('La fecha y hora ingresada no pueden ser futuras.')
            return value

        def create(self, validated_data):

            # Obtengo datos ingresados.
            fechaHora = validated_data['fechaHora']
            foto = validated_data.get('foto', None)
            descripcion = validated_data.get('descripcion', '')
            estado_sentimiento = validated_data.get('estado', None)
            registro = usuario.donante.registro

            lugar_donacion = obtener_lugar_donacion(validated_data)

            # Creo objeto donación
            donacion = Donacion.objects.create(
                fechaHora=fechaHora,
                foto=foto,
                registro=registro,
                descripcion=descripcion,
                lugarDonacion=lugar_donacion,
                estado=estado_sentimiento
                )

            # Seteo estado 'Sin verificar' a la donación.
            estado = EstadoDonacion.objects.get(nombre='Sin verificar')

            historico = HistoricoEstadoDonacion(
                inicio=datetime.datetime.now(),
                estado=estado,
                donacion=donacion
                )

            historico.save()

            return donacion

        def update(self, instance, validated_data):
            if instance.historicoEstados:
                ultimo_historico_donacion = instance.historicoEstados.latest('inicio')
                ultimo_estado = ultimo_historico_donacion.estado.nombre
                if ultimo_estado.lower() == ESTADO_VERIFICADA:
                    raise ValidationError('No puedes actualizar la información de una imagen ya verificada.')

            instance.fechaHora = validated_data.get('fechaHora', instance.fechaHora)
            instance.descripcion = validated_data.get('descripcion', instance.descripcion)
            instance.estado = validated_data.get('estado', instance.estado)

            foto_nueva = validated_data.get('foto', None)

            # Si existe nueva foto la seteo a la instancia.
            if foto_nueva is not None:
                if instance.foto:
                    instance.foto.delete()
                instance.foto = foto_nueva

            nuevo_lugar_donacion = obtener_lugar_donacion(validated_data)

            instance.lugarDonacion = nuevo_lugar_donacion

            instance.save()
            return instance

    return DonacionCreateUpdateDestroySerializer


class DonacionSerializer(ModelSerializer):
    lugarDonacion = LugarDonacionSerializer()
    estado_donacion = SerializerMethodField()

    class Meta:
        model = Donacion
        depth = 2
        fields = [
            'id',
            'fechaHora',
            'registro',
            'foto',
            'estado_donacion',
            'imagen_verificacion',
            'lugarDonacion',
            'descripcion',
            'estado'
        ]

    def get_estado_donacion(self, obj):
        ultimo_historico_donacion = obj.historicoEstados.latest('inicio')
        return ultimo_historico_donacion.estado.nombre


class RegistroDonacionSerializer(ModelSerializer):
    donaciones = DonacionSerializer(many=True)

    class Meta:
        model = RegistroDonacion
        fields = [
            'id',
            'donaciones'
        ]
        depth = 1


class VerificarImagenDonacionSerializer(ModelSerializer):
    class Meta:
        model = Donacion
        fields = [
            'imagen_verificacion'
        ]

    def validate(self, data):
        donacion = self.instance
        if donacion.historicoEstados:
            ultimo_historico_donacion = donacion.historicoEstados.latest('inicio')
            ultimo_estado = ultimo_historico_donacion.estado.nombre
            if ultimo_estado.lower() == ESTADO_VERIFICADA:
                raise ValidationError('No puedes subir una imagen de verificación porque esta donación ya se encuentra verificada.')

        return data

    def update(self, instance, validated_data):
        # Obtengo los datos ingresados.
        instance.imagen_verificacion = validated_data.get('imagen_verificacion', instance.imagen_verificacion)

        # Obtengo el último histórico de la donación y seteo
        # su fecha fin con la fecha actual.
        ultimo_historico_donacion = instance.historicoEstados.last()
        ultimo_historico_donacion.fin = datetime.datetime.now()
        ultimo_historico_donacion.save()

        # Creo nuevo histórico con estado 'Pendiente' y fecha inicio
        # con fecha actual y lo asocio a la donación.
        estado = EstadoDonacion.objects.get(nombre='Pendiente')

        HistoricoEstadoDonacion.objects.create(
            inicio=datetime.datetime.now(),
            estado=estado,
            donacion=instance
            )

        instance.save()

        return instance
