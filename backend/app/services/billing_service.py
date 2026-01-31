import os

class BillingService:
    @staticmethod
    async def create_checkout_session(customer_email: str, plan: str):
        """Placeholder for Stripe checkout session creation.
        Implement Stripe SDK integration here for real payments.
        """
        if os.getenv('TEST_MODE') == '1':
            return {"url": f"https://stripe.test/checkout?plan={plan}&email={customer_email}"}
        # In production: create session via stripe SDK
        raise NotImplementedError("Stripe integration not yet implemented")
