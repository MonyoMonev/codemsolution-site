#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерира английската версия на сайта:  index.html (БГ, източник)  →  en/index.html

    python3 _build_en.py

Как работи: всеки елемент с data-i18n="ключ" получава английския текст от речника EN
по-долу. Елементи с data-i18n-attr="content" се превеждат в атрибута (meta тагове).
Текст без ключ остава както е (имейл, телефон, ЕИК, App Store…).
Пускай го след ВСЯКА промяна на index.html, иначе английската версия изостава.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "index.html")
OUT  = os.path.join(HERE, "en", "index.html")

EN = {
  # --- meta ---
  "meta.title":   "Codem Solution | software, apps, systems and automation",
  "meta.desc":    "Codem Solution builds mobile apps, websites, business systems and automations. Direct contact with the developer, fixed price, reply within 24 hours.",
  "meta.ogtitle": "Codem Solution | software for your business",
  "meta.ogdesc":  "Apps, websites, systems and automation. Direct contact with the developer, fixed price.",
  "meta.locale":  "en_US",
  # --- nav ---
  "nav.why": "Why us", "nav.services": "Services", "nav.process": "How we work", "nav.contact": "Contact",
  "nav.cta": "Get a quote",
  # --- hero ---
  "hero.tag": "Apps · websites · systems · automation",
  "hero.l1": "Software for your&nbsp;business",
  "hero.l2": "that impresses",
  "hero.l3": "from the first second.",
  "hero.p":  "Like this website. Mobile apps, websites, internal systems and automations: whatever your business needs to run faster and tidier. You talk directly to the person who will build it.",
  "hero.cta1": "Let's talk about your idea",
  "hero.cta2": "Why Codem",
  "hero.n1b": "Within 24 hours", "hero.n1": "reply to every enquiry",
  "hero.n2b": "Fixed price",     "hero.n2": "before we start",
  "hero.n3b": "iOS + Android",   "hero.n3": "from one codebase",
  "hero.scroll": "scroll",
  "chip.1": "iOS and Android", "chip.2": "App store publishing", "chip.3": "Website on your domain", "chip.4": "Support afterwards",
  # --- marquee ---
  "mq.1": "Mobile apps", "mq.2": "Websites", "mq.3": "Business systems", "mq.4": "Automation", "mq.5": "Backend and integrations", "mq.8": "Support",
  # --- why ---
  "why.tag": "Why Codem Solution",
  "why.h2":  "Four things big agencies can't promise you.",
  "why.1h": "You talk to the developer",
  "why.1p": "Not to a sales manager. The person answering your email is the one who will write the code. No “I'll pass it on to the team”.",
  "why.2h": "The price is fixed",
  "why.2p": "We state it before the start, in writing, and it doesn't change halfway. No billable hours, no surprises at the end.",
  "why.3h": "Reply within 24 hours",
  "why.3p": "To every enquiry, to every note on the project. Ask on Monday, you have an answer on Tuesday.",
  "why.4h": "Support doesn't end",
  "why.4p": "After launch we stay around for updates, new features and questions. We don't hand over the project and disappear.",
  # --- services ---
  "svc.tag": "What we do",
  "svc.h2":  "Whatever you need. All the way.",
  "svc.lead": "An app, a website, a system or an automation. From the idea to launch, without passing you on to third parties.",
  "svc.1h": "Mobile apps",
  "svc.1p": "For iOS and Android from one codebase. We handle publishing too, including Apple's review, where most apps get rejected.",
  "svc.1a": "Subscriptions and payments", "svc.1b": "Notifications and profiles", "svc.1c": "App Store and Google Play",
  "svc.2h": "Websites",
  "svc.2p": "Fast, on your own domain, looking good on a phone. Plus a Google Business profile so people find you locally.",
  "svc.2a": "Own domain and email", "svc.2b": "Google Business and SEO basics", "svc.2c": "Monthly maintenance",
  "svc.3h": "Business systems",
  "svc.3p": "Your own software for clients, orders, stock, schedules and reports. A backend that keeps everything in one place, built around how you actually work.",
  "svc.3a": "CRM, orders, inventory", "svc.3b": "Team roles, from phone and desktop", "svc.3c": "Reports that build themselves",
  "svc.4h": "Automation",
  "svc.4p": "Repetitive work done by itself. We connect the tools you already use so data flows without manual copying.",
  "svc.4a": "Invoices, emails and spreadsheets, automatically", "svc.4b": "Links between software and platforms", "svc.4c": "Alerts when something needs attention",
  # --- process ---
  "proc.tag": "How we work",
  "proc.h2":  "Four steps. Not a single surprise.",
  "proc.1h": "Conversation", "proc.1p": "You tell us. We say honestly what's realistic.",
  "proc.2h": "Quote",        "proc.2p": "Price and deadline in writing, before you pay anything.",
  "proc.3h": "Development",  "proc.3p": "You see progress along the way. Changes are part of the job.",
  "proc.4h": "Launch",       "proc.4p": "We publish, hand over, and stay around.",
  # --- contact ---
  "ct.tag": "Contact",
  "ct.h2":  "Tell us your idea.",
  "ct.lead": "We reply within one working day, with questions or straight away with an indicative price. We work with clients in Bulgaria and abroad.",
  "ct.addr": "82 Ivaylo St., Odesos, Varna, Bulgaria",
  "legal.h": "Company details",
  "legal.firm": "Company", "legal.firmv": "SIMBI25 EOOD (Ltd.)",
  "legal.eik": "Company ID (EIK)",
  "legal.seat": "Registered office", "legal.seatv": "82 Ivaylo St., Odesos, 9000 Varna, Bulgaria",
  "legal.mgr": "Managing director", "legal.mgrv": "Monyo Monev",
  "foot.firm": "SIMBI25 EOOD · Company ID 208966434",
  "foot.loc": "Varna, Bulgaria",
}

def build():
    s = io.open(SRC, encoding="utf-8").read()
    missing, used = [], set()

    # 1) атрибути (meta content)
    def attr_sub(m):
        key = m.group(2); used.add(key)
        if key not in EN: missing.append(key); return m.group(0)
        tag = m.group(0)
        return re.sub(r'content="[^"]*"', 'content="%s"' % EN[key].replace('"', '&quot;'), tag, count=1)
    s = re.sub(r'<meta[^>]*data-i18n-attr="content"[^>]*data-i18n="([^"]+)"[^>]*>', lambda m: attr_sub(type('M',(),{'group':lambda self,i:(m.group(0) if i==0 else m.group(1))})()), s)

    # 2) текстово съдържание:  <tag ... data-i18n="key" ...>ТЕКСТ</tag>
    def text_sub(m):
        open_tag, key, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
        used.add(key)
        if key not in EN: missing.append(key); return m.group(0)
        return open_tag + EN[key] + close
    s = re.sub(r'(<(?:title|a|span|p|h1|h2|h3|li|div|b|em|dt|dd)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)(.*?)(</(?:title|a|span|p|h1|h2|h3|li|div|b|em|dt|dd)>)',
               text_sub, s, flags=re.S)

    # 3) език на документа, бутон за език, hreflang
    s = s.replace('<html lang="bg">', '<html lang="en">', 1)
    s = s.replace('<a href="en/" class="lang" id="langSwitch" hreflang="en" lang="en" title="English">EN</a>',
                  '<a href="../" class="lang" id="langSwitch" hreflang="bg" lang="bg" title="Български">BG</a>', 1)
    s = s.replace('<link rel="alternate" hreflang="bg" href="https://codemsolution.com/">', '<link rel="alternate" hreflang="bg" href="https://codemsolution.com/">', 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(s)

    unused = sorted(set(EN) - used)
    print("en/index.html: %d байта" % len(s.encode("utf-8")))
    print("ключове преведени: %d" % len(used))
    if missing: print("ЛИПСВАТ В РЕЧНИКА (останаха на БГ):", sorted(set(missing)))
    if unused:  print("в речника, но не в HTML:", unused)
    left = re.findall(r'[А-Яа-я]{3,}', re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S))
    if left: print("ОСТАНАЛА КИРИЛИЦА в EN версията:", sorted(set(left))[:20])
    return 0 if not missing else 1

if __name__ == "__main__":
    sys.exit(build())
