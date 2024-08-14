import argparse
import numpy_financial as npf

def calculate_loan_info(principal, rate, years, payment, extra_payment=0, lump_sum=0):
    # Рассчитываем месячную процентную ставку
    monthly_rate = rate / 100 / 12
    # Исходное количество месяцев (срок кредита)
    nper_initial = years * 12

    # Рассчитываем переплату и срок для исходного платежа
    total_payment_initial = payment * nper_initial
    overpayment_initial = total_payment_initial - principal

    # Если есть единовременный платеж, уменьшаем сумму кредита
    if lump_sum > 0:
        principal -= lump_sum

    # Рассчитываем новый срок кредита с учетом увеличенного платежа
    nper_new = npf.nper(monthly_rate, -extra_payment, principal)
    total_payment_new = extra_payment * nper_new + lump_sum
    overpayment_new = total_payment_new - principal

    # Рассчитываем сокращение срока и переплаты
    reduction_in_months = nper_initial - nper_new
    reduction_in_years = int(reduction_in_months // 12)
    reduction_in_months = int(reduction_in_months % 12)

    reduction_in_overpayment = overpayment_initial - overpayment_new

    return {
        "initial_overpayment": overpayment_initial,
        "new_overpayment": overpayment_new,
        "reduction_in_overpayment": reduction_in_overpayment,
        "reduction_in_years": reduction_in_years,
        "reduction_in_months": reduction_in_months,
        "total_payment_initial": total_payment_initial,
        "total_payment_new": total_payment_new
    }

def main():
    parser = argparse.ArgumentParser(description="Calculate mortgage overpayment and term reduction.")
    parser.add_argument("--principal", type=float, required=True, help="Initial loan amount (principal)")
    parser.add_argument("--rate", type=float, required=True, help="Annual interest rate in percent")
    parser.add_argument("--years", type=int, required=True, help="Term of the loan in years")
    parser.add_argument("--payment", type=float, required=True, help="Initial monthly payment")
    parser.add_argument("--extra_payment", type=float, required=True, help="Increased monthly payment")
    parser.add_argument("--lump_sum", type=float, default=0, help="One-time additional payment (optional)")

    args = parser.parse_args()

    result = calculate_loan_info(
        principal=args.principal,
        rate=args.rate,
        years=args.years,
        payment=args.payment,
        extra_payment=args.extra_payment,
        lump_sum=args.lump_sum
    )

    print(f"Initial Overpayment: {result['initial_overpayment']:.2f} RUB")
    print(f"New Overpayment: {result['new_overpayment']:.2f} RUB")
    print(f"Reduction in Overpayment: {result['reduction_in_overpayment']:.2f} RUB")
    print(f"Reduction in Term: {result['reduction_in_years']} years, {result['reduction_in_months']} months")
    print(f"Total Payment (Initial): {result['total_payment_initial']:.2f} RUB")
    print(f"Total Payment (New): {result['total_payment_new']:.2f} RUB")

if __name__ == "__main__":
    main()