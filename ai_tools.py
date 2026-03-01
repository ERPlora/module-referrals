"""AI tools for the Referrals module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListReferrals(AssistantTool):
    name = "list_referrals"
    description = "List referrals."
    module_id = "referrals"
    required_permission = "referrals.view_referral"
    parameters = {"type": "object", "properties": {"status": {"type": "string", "description": "pending, converted, rewarded, expired"}, "limit": {"type": "integer"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from referrals.models import Referral
        qs = Referral.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"referrals": [{"id": str(r.id), "referrer_name": r.referrer_name, "referred_name": r.referred_name, "referral_code": r.referral_code, "status": r.status, "reward_given": r.reward_given} for r in qs[:limit]]}


@register_tool
class CreateReferral(AssistantTool):
    name = "create_referral"
    description = "Create a referral."
    module_id = "referrals"
    required_permission = "referrals.add_referral"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "referrer_name": {"type": "string"}, "referrer_email": {"type": "string"},
            "referred_name": {"type": "string"}, "referred_email": {"type": "string"},
            "referral_code": {"type": "string"},
        },
        "required": ["referrer_name", "referred_name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from referrals.models import Referral
        r = Referral.objects.create(referrer_name=args['referrer_name'], referrer_email=args.get('referrer_email', ''), referred_name=args['referred_name'], referred_email=args.get('referred_email', ''), referral_code=args.get('referral_code', ''))
        return {"id": str(r.id), "referral_code": r.referral_code, "created": True}
