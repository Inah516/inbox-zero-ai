"""Pre-baked email batches for evaluators / demo. No real PII — all synthetic."""

EXAMPLE_BATCHES = {
    "monday_morning": {
        "title": "Monday Morning Inbox",
        "tagline": "Mixed bag — work asks, a meeting reschedule, and noise.",
        "emails": [
            {
                "from": "Linda Hartwell <linda@northwind-legal.com>",
                "subject": "URGENT: Vendor MSA — review needed before EOD",
                "date": "2026-05-18T08:42:00+07:00",
                "body": (
                    "Hi,\n\nI need your sign-off on the redlined MSA before 5pm today — "
                    "procurement is gating the PO on it. Two items I flagged:\n\n"
                    "1. Termination-for-convenience window is 60 days; we usually do 30.\n"
                    "2. Liability cap is 12x fees, not 1x.\n\n"
                    "If those are acceptable, just reply 'go' and I'll counter-sign.\n\n"
                    "— Linda"
                ),
            },
            {
                "from": "TechCrunch Daily <newsletter@techcrunch.com>",
                "subject": "🦾 The robotaxi war just got weirder",
                "date": "2026-05-18T07:00:00+07:00",
                "body": "Top stories of the day...\n[long newsletter content omitted]",
            },
            {
                "from": "Marco Tan <marco@designstudio.io>",
                "subject": "Coffee Wed or Thu?",
                "date": "2026-05-18T06:15:00+07:00",
                "body": (
                    "Hey, in town this week — got time for coffee Wed afternoon or "
                    "Thu morning? My calendar's flexible. — M"
                ),
            },
            {
                "from": "AWS Billing <no-reply@aws.amazon.com>",
                "subject": "Your AWS Invoice for April 2026",
                "date": "2026-05-18T03:11:00+00:00",
                "body": "Total: $2,184.20. View invoice at console.aws.amazon.com/billing",
            },
            {
                "from": "Priya Shah <priya.shah@portfolioco.vc>",
                "subject": "Re: Series B intro — pushed to Friday 10am",
                "date": "2026-05-18T07:55:00+07:00",
                "body": (
                    "Quick note — partner got pulled into a board meeting, so we're "
                    "moving the intro from Wed 3pm to Fri 10am SGT. Same dial-in. "
                    "Confirm if that works, otherwise I'll shop another slot.\n\n— P"
                ),
            },
            {
                "from": "GitHub <noreply@github.com>",
                "subject": "[acmecorp/api-gateway] Vulnerability alert: high severity",
                "date": "2026-05-18T02:01:00+00:00",
                "body": (
                    "A high severity vulnerability has been detected in the dependency "
                    "graph for acmecorp/api-gateway: CVE-2026-12345 in fastify-cors@9.0.1.\n"
                    "Recommended: upgrade to 9.1.0 or later."
                ),
            },
            {
                "from": "Eddie (Sales) <eddie@somevendor.com>",
                "subject": "Quick demo? 15 min, promise",
                "date": "2026-05-17T22:14:00+07:00",
                "body": (
                    "Saw you signed up last quarter — would love 15 min to walk through "
                    "our new agent eval suite. Tomorrow 4pm work?"
                ),
            },
        ],
    },
    "founder_chaos": {
        "title": "Founder Chaos Hour",
        "tagline": "Investor reply, candidate decline, vendor escalation, and a fire.",
        "emails": [
            {
                "from": "Owen Kim <owen@frontiercapital.vc>",
                "subject": "Re: Term sheet — two redlines",
                "date": "2026-05-18T09:02:00+07:00",
                "body": (
                    "Two redlines from our side:\n"
                    "  1. Pro rata extends to Series C only (not D+)\n"
                    "  2. Information rights gated at $500K ARR\n\n"
                    "If those are workable we can sign by Friday. — Owen"
                ),
            },
            {
                "from": "Selin Ozdemir <selin.ozdemir@protonmail.com>",
                "subject": "Withdrawing from the engineering loop",
                "date": "2026-05-18T07:40:00+07:00",
                "body": (
                    "Hi — appreciate the conversations so far, but I've accepted an "
                    "offer elsewhere and need to withdraw from your loop. Hope our "
                    "paths cross again. — Selin"
                ),
            },
            {
                "from": "Renee at Stripe <renee.k@stripe.com>",
                "subject": "Action required: re-verify EU operating entity by May 25",
                "date": "2026-05-17T23:11:00+00:00",
                "body": (
                    "Compliance flagged your EU entity for re-verification. Upload an "
                    "updated certificate of incorporation by 25 May. Failure to do so "
                    "will pause EU payouts."
                ),
            },
            {
                "from": "PagerDuty <alerts@pagerduty.com>",
                "subject": "[INCIDENT 4291] Resolved: Checkout 5xx surge — 14 min",
                "date": "2026-05-18T04:22:00+00:00",
                "body": "Auto-resolved at 04:22Z. RCA pending from on-call.",
            },
            {
                "from": "Carla Diaz <carla@growthlab.co>",
                "subject": "Speaking spot — TechWeek SG, Aug 12 keynote",
                "date": "2026-05-18T05:00:00+07:00",
                "body": (
                    "We'd love to have you keynote the AI day at TechWeek SG on Aug 12. "
                    "Honorarium $4k + travel. Need confirmation by next Mon."
                ),
            },
        ],
    },
    "vacation_aftermath": {
        "title": "Back from Vacation",
        "tagline": "47 unread distilled into the 6 you can't ignore.",
        "emails": [
            {
                "from": "Anika Rao <anika.rao@boardops.io>",
                "subject": "Q2 board pre-read due Friday",
                "date": "2026-05-18T03:00:00+00:00",
                "body": "Reminder: pre-read draft due to me by Fri so packets ship Sun.",
            },
            {
                "from": "Tomas L. <tomas@infraco.io>",
                "subject": "Production DB migration — your sign-off",
                "date": "2026-05-17T13:00:00+00:00",
                "body": (
                    "We're cutting over the analytics DB Wed 2am SGT. I have read-only "
                    "fallback ready. Need your written sign-off before we kick off."
                ),
            },
            {
                "from": "Indeed <jobs@indeed.com>",
                "subject": "5 new candidates for 'Senior Backend Engineer'",
                "date": "2026-05-17T14:00:00+00:00",
                "body": "Top matches from the past 24 hours...",
            },
            {
                "from": "Maya P. (your COS) <maya@yourco.com>",
                "subject": "Calendar this week — please review",
                "date": "2026-05-18T01:30:00+00:00",
                "body": (
                    "Tight week — 14 meetings booked. I've flagged 3 you might want to "
                    "decline. Reply 'review' and I'll send the proposed cuts."
                ),
            },
            {
                "from": "Sam (Customer) <sam@bigcustomer.co>",
                "subject": "Renewal at risk — pricing concerns",
                "date": "2026-05-17T22:00:00+00:00",
                "body": (
                    "Need to talk before the 15-Jun renewal. Our finance is pushing "
                    "back on the 22% uplift. Can we get on a call this week?"
                ),
            },
            {
                "from": "Lin Wei <lin@hrops.io>",
                "subject": "FYI — anonymous engineering pulse came in",
                "date": "2026-05-17T16:00:00+00:00",
                "body": (
                    "Pulse score dipped 0.4 — main theme is 'unclear roadmap'. "
                    "I'll send the full breakdown after our 1:1."
                ),
            },
        ],
    },
    "support_queue": {
        "title": "Support Queue Review",
        "tagline": "5 customer threads. 1 churn flag, 2 quick wins, 2 noise.",
        "emails": [
            {
                "from": "Jamal Ali <jamal@useracmeco.com>",
                "subject": "API 429s every Monday morning",
                "date": "2026-05-18T01:00:00+00:00",
                "body": (
                    "We're getting rate-limited starting around 9am SGT every Mon. "
                    "Bumped to plan-pro last month — was told limits would 10x. Help?"
                ),
            },
            {
                "from": "Hye-Jin Park <hyejin@studio-park.kr>",
                "subject": "Cancellation request",
                "date": "2026-05-18T02:00:00+00:00",
                "body": "Please cancel my subscription effective end of cycle. Thanks.",
            },
            {
                "from": "Marc Beaumont <marc@labbeaumont.fr>",
                "subject": "Feature request: bulk export CSV",
                "date": "2026-05-17T20:00:00+00:00",
                "body": "Would be huge for our reporting workflow. Any timeline?",
            },
            {
                "from": "Nadia A. <nadia@orgnadia.com>",
                "subject": "How do I reset my password?",
                "date": "2026-05-18T00:30:00+00:00",
                "body": "Hi — can't find the link. Help?",
            },
            {
                "from": "Compliance <compliance@enterpriseco.com>",
                "subject": "SOC2 type II report request",
                "date": "2026-05-17T18:00:00+00:00",
                "body": "Vendor onboarding — please share your latest SOC2 type II.",
            },
        ],
    },
    "single_complex": {
        "title": "Single Complex Email",
        "tagline": "One dense email — see how the agents tear it apart.",
        "emails": [
            {
                "from": "Aldo Marchetti <aldo.m@bigaccount.com>",
                "subject": "Re: Migration plan — concerns + must-haves",
                "date": "2026-05-18T08:30:00+02:00",
                "body": (
                    "Thanks for the deck yesterday. After internal review, three "
                    "blockers and two requests:\n\n"
                    "BLOCKERS\n"
                    " 1. Data residency: our dataset must stay in EU — your proposed "
                    "    region (us-east-1) is a non-starter.\n"
                    " 2. Downtime: 4h cutover window won't pass change-board. We need "
                    "    < 30 min, ideally zero-downtime via dual-write.\n"
                    " 3. Audit logs: we need immutable WORM storage for all admin "
                    "    actions, retention 7y.\n\n"
                    "REQUESTS\n"
                    " A. SSO via our Entra ID tenant (we'll provide metadata XML).\n"
                    " B. SLA bumped to 99.95% with credits at 99.9%.\n\n"
                    "Can we get a written response by Tuesday EOB? Our exec sponsor "
                    "needs it for the May 27 steering committee.\n\n"
                    "— Aldo"
                ),
            },
        ],
    },
}
