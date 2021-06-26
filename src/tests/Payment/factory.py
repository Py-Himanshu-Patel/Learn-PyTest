import factory

from apps.Payment.models import Transaction, Currency
from faker import Faker
fake = Faker()


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        # this make sure that if a repeated value is 
        # passed in these two fields then same obj is returned
        # without causing any duplicacy error

        # django_get_or_create = ('name', 'code')


    # code and name get assigned when the class is called hence if we use
    # create_batch(n) we get all n object same
 
    # code, name = fake.currency() 

    # Since currency is declared as a parameter, it won't be passed to 
    # the model (it's automatically added to Meta.exclude.
    class Params:
        currency = factory.Faker("currency")  # (code, name)

    code = factory.LazyAttribute(lambda o: o.currency[0])
    name = factory.LazyAttribute(lambda o: o.currency[1])
    symbol = '$'


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    
    # if we do not assign these attributes here then they will remain blank
    
    # currency is auto generated on creation of transaction
    currency = factory.SubFactory(CurrencyFactory)
    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.name())


class FilledTransactionFactory(factory.django.DjangoModelFactory):
    ''' Transaction obj with 'payment_intent_id' field assigned '''
    class Meta:
        model = Transaction

    currency = factory.SubFactory(CurrencyFactory)
    payment_intent_id = "abcdef"
    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.name())
    message = fake.text()[:20].strip()


class CurrencylessTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    
    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.name())
    message = fake.text()[:20].strip()
