from django.shortcuts import render
from decimal import Decimal
from .services import calculate_premium_logic

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer, Policy, Claim, ActionRequest
from .serializers import CustomerSerializer

@api_view(['POST'])
def create_customer(request):

    name = request.data.get('name')
    email = request.data.get('email')
    wallet_balance = Decimal(
        request.data.get('wallet_balance')
    )

    customer = Customer.objects.create(
        name=name,
        email=email,
        wallet_balance=wallet_balance
    )

    premium = Decimal("50")

    status = (
        "ACTIVE"
        if wallet_balance >= premium
        else "PENDING"
    )

    Policy.objects.create(
        customer=customer,
        policy_type="Delivery",
        premium_amount=premium,
        status=status
    )

    serializer = CustomerSerializer(customer)

    return Response(
        serializer.data,
        status=201
    )

@api_view(['POST'])
def calculate_premium(request):

   age = request.data.get('age')
   vehicle_type = request.data.get('vehicle_type')
   accidents = request.data.get('accidents', 0)

    # validation
   if age is None or vehicle_type is None:
        return Response(
            {"error": "age and vehicle_type are required"},
            status=400
        )

   try:
        age = int(age)
        accidents = int(accidents)
   except ValueError:
        return Response(
            {"error": "age and accidents must be numbers"},
            status=400
        )

    #  BUSINESS LOGIC MOVED OUTSIDE VIEW
   premium = calculate_premium_logic(age, vehicle_type, accidents)
   return Response({
        "age": age,
        "vehicle_type": vehicle_type,
        "accidents": accidents,
        "final_premium": premium
    }, status=200)

@api_view(['GET'])
def get_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

@api_view(['POST'])
def create_claim(request):

    policy_id = request.data.get('policy_id')
    amount = float(request.data.get('amount'))
    description = request.data.get('description')

    policy = Policy.objects.get(id=policy_id)

    claim = Claim.objects.create(
        policy=policy,
        amount=amount,
        description=description,
        priority="HIGH_PRIORITY" if amount > 500 else "NORMAL"
    )

    policy.status = "UNDER_REVIEW"
    policy.save()

    return Response({
        "id": claim.id,
        "status": "UNDER_REVIEW",
        "priority": claim.priority
    })

@api_view(['POST'])
def renew_policy(request):

    key = request.headers.get('Idempotency-Key')

    if not key:
        return Response(
            {"error": "Idempotency-Key required"},
            status=400
        )

    if ActionRequest.objects.filter(
        idempotency_key=key
    ).exists():
        return Response(
            {"message": "Already processed"},
            status=200
        )

    ActionRequest.objects.create(
        idempotency_key=key
    )

    policy_id = request.data.get('policy_id')

    try:
        policy = Policy.objects.get(id=policy_id)
    except Policy.DoesNotExist:
        return Response(
            {"error": "Policy not found"},
            status=404
        )

    policy.status = "ACTIVE"
    policy.save()

    return Response(
        {
            "message": "Policy renewed successfully",
            "policy_id": policy.id,
            "status": policy.status
        },
        status=201
    )