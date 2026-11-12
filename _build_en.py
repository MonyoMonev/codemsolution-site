#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерира английската версия на сайта:  index.html (БГ, източник)  ->  en/index.html

    python3 _build_en.py

Всеки елемент с data-i18n="ключ" получава английския текст от речника EN по-долу.
Мета таговете с data-i18n-attr="content" се превеждат в атрибута.
Текст без ключ остава какъвто е (имейл, телефон, ЕИК, App Store, суми в €).
Пускай го след ВСЯКА промяна на index.html, иначе английската версия изостава.
В текстовете няма тирета нарочно: Моньо не ги иска, изглеждат писани от AI.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
OUT = os.path.join(HERE, "en", "index.html")

EN = {
  # --- meta ---
  "meta.title": "Custom software, mobile apps and websites | Codem Solution",
  "meta.desc": "We build business systems, mobile apps and websites and automate manual work. You work directly with the developer, at a price agreed in advance.",
  "meta.ogtitle": "Codem Solution | Software made to measure for your company",
  "meta.ogdesc": "Business systems, mobile apps, websites and automation. You work directly with the developer, at a price agreed in advance.",
  "meta.locale": "en_US",
  # --- nav ---
  "nav.services": "Services", "nav.why": "Why us", "nav.process": "How we work", "nav.contact": "Contact",
  "nav.cta": "Get a quote",
  # --- hero ---
  "hero.tag": "Software development",
  "hero.l1": "Software made to measure",
  "hero.l2": "for your company.",
  "hero.p": "We build business systems, mobile apps and websites, and automate the work your team still does by hand. Scroll down to see what it looks like from the inside.",
  "hero.cta1": "Let's talk about your project",
  "hero.cta2": "See inside",
  "hero.cue": "Scroll",
  # --- system in the laptop ---
  "dash.brand": "Your company",
  "dash.n1": "Dashboard", "dash.n2": "Orders", "dash.n3": "Customers", "dash.n4": "Stock", "dash.n5": "Reports",
  "dash.title": "Dashboard", "dash.today": "Today",
  "dash.k1": "Orders today", "dash.k2": "Revenue", "dash.k3": "New customers",
  "dash.chart": "Orders this week",
  "d.1": "Mon", "d.2": "Tue", "d.3": "Wed", "d.4": "Thu", "d.5": "Fri", "d.6": "Sat", "d.7": "Sun",
  "dash.list": "Latest orders",
  "nm.1": "Ivan Petrov", "nm.2": "Maria Koleva", "nm.3": "Georgi Dimov", "nm.4": "Elena Stoyanova",
  "st.paid": "Paid", "st.sent": "Shipped", "st.new": "New",
  "dash.toast": "New order #1043",
  # --- app in the phone ---
  "app.nt": "New booking", "app.nb": "Elena, tomorrow at 11:30",
  "app.brand": "Your app", "app.hi": "Hi, Maria",
  "app.next": "Next client", "app.when": "Today, 18:30", "app.what": "Ivan, haircut", "app.ok": "Confirm",
  "app.free": "Free slots",
  # --- website in the browser ---
  "br.url": "yourcompany.com", "br.brand": "Your company",
  "br.l1": "Home", "br.l2": "Services", "br.l3": "Contact",
  "br.h": "Your business, open day and night.",
  "br.p": "A website that opens fast on any phone and brings customers straight to you.",
  "br.btn": "Call us",
  "br.f1": "Loads fast", "br.f2": "Found on Google", "br.f3": "Easy to update",
  # --- automation ---
  "fl.1": "New order", "fl.2": "Invoice", "fl.3": "Email to the customer", "fl.4": "Report in the spreadsheet",
  "fl.done": "It all happens in seconds, with no manual entry.",
  # --- captions ---
  "cs.h": "Business systems",
  "cs.p": "Software built around the way you work. Orders, customers, stock and reports live in one place, on your phone and on your computer.",
  "cs.t1": "Orders", "cs.t2": "Stock", "cs.t3": "Reports",
  "ca.h": "Mobile apps",
  "ca.p": "One app for iPhone and Android. We also take care of publishing on the App Store and Google Play, including both store reviews.",
  "ca.t3": "Payments",
  "cw.h": "Websites",
  "cw.p": "A website on your own domain that opens fast and looks good on a phone. We also set up your Google profile so local customers can find you.",
  "cw.t1": "Domain and email", "cw.t3": "Maintenance",
  "cu.h": "Automation",
  "cu.p": "We connect the tools you already work with. Invoices, emails and reports are prepared automatically and nobody retypes data by hand.",
  "cu.t1": "Invoices", "cu.t2": "Emails", "cu.t3": "Spreadsheets",
  # --- marquee ---
  "mq.1": "Business systems", "mq.2": "Mobile apps", "mq.3": "Websites", "mq.4": "Automation", "mq.7": "Maintenance", "mq.8": "Over 10 years of experience",
  # --- why ---
  "why.tag": "Why Codem Solution",
  "why.h2": "What you can expect from us.",
  "why.lead1": "Over 10 years in the IT sector.", "why.lead2": "That is the experience of the people on our team.",
  "why.1h": "You talk to the developer",
  "why.1p": "Your questions go straight to the person who writes the code. There are no salespeople or middlemen in between.",
  "why.2h": "The price is known in advance",
  "why.2p": "You get it in writing before we start. If the scope doesn't change, neither does the price.",
  "why.3h": "A reply within one working day",
  "why.3p": "That's how long you wait for an answer to an enquiry, a question or a note on the project.",
  "why.4h": "We stay after launch",
  "why.4p": "We maintain what we build. We update it, add new features and fix problems if they appear.",
  # --- process ---
  "proc.tag": "How we work",
  "proc.h2": "From the first conversation to the finished product.",
  "proc.1h": "Conversation", "proc.1p": "You tell us what you need. We tell you what can be done, how long it takes and what it costs.",
  "proc.2h": "Quote", "proc.2p": "You get the price, the deadline and a precise description of the work in writing.",
  "proc.3h": "Development", "proc.3p": "We show you the work in stages, so you can comment in time.",
  "proc.4h": "Launch", "proc.4p": "We publish the product, show you how to use it and take over the maintenance.",
  # --- contact ---
  "ct.tag": "Contact",
  "ct.h2": "Let's talk.",
  "ct.lead": "Call or write to us. We reply within one working day.",
  "ct.mail": "Email", "ct.tel": "Phone",
  "foot.co": "Company details",
}

# --- редакция на текстовете от 12.11.2026: услуги, защо ние, процес, технологии, въпроси ---
EN.update({
  "cs.p": "A system built around your processes. Orders, customers, stock and reports live in one place, and each employee sees only what they need.",
  "cs.t1": "Orders", "cs.t2": "Roles and access", "cs.t3": "Reports",
  "ca.p": "One app for iPhone and Android. We handle the whole path to the stores: preparing, submitting and getting the app approved on the App Store and Google Play.",
  "ca.t1": "Payments", "ca.t2": "Notifications", "ca.t3": "Maps and location",
  "cw.p": "A website on your own domain that loads fast and reads well on a phone. We set up your company email, your Google profile and your presence in search.",
  "cw.t2": "Google profile",
  "cu.p": "We connect the tools you already work with. Invoices, emails and reports are prepared automatically and nobody retypes data by hand.",
  "cu.t3": "Reports",
  "fl.4": "Row in the spreadsheet",
  "why.1h": "You work directly with the developer",
  "why.1p": "Your questions go straight to the person who writes the code. There are no salespeople or middlemen in between.",
  "why.2h": "Price and deadline agreed in advance",
  "why.2p": "You get them in writing before we start. If the scope doesn't change, the price stays the same.",
  "why.3h": "A reply within one working day",
  "why.3p": "We answer an enquiry, a question or a note on the project within one working day.",
  "why.4h": "One team for the whole solution",
  "why.4p": "The system, the mobile app and the website are built by one team and work together. You don't have to coordinate several contractors.",
  "why.5h": "We stay after launch",
  "why.5p": "We maintain what we build: we update it, add new features and fix problems that come up.",
  "proc.got": "You get",
  "proc.1p": "You tell us what you need and how you work today. We tell you what can be done, how long it takes and what budget it needs.",
  "proc.1g": "A clear project scope",
  "proc.2p": "You get a written quote with the price, the deadline and a description of everything that will be built.",
  "proc.2g": "A quote with a fixed price",
  "proc.3p": "We work in stages. After each one we show you a working version, so you can comment in time.",
  "proc.3g": "A working version after each stage",
  "proc.4p": "We publish the product, show your team how to use it and take over the maintenance.",
  "proc.4g": "A finished product and maintenance",
  "tech.tag": "Technology",
  "tech.h2": "We work with proven technology.",
  "tech.p": "We choose widely used technologies with long term support, so your product can keep growing for years.",
  "tech.g1": "Mobile apps", "tech.g2": "Systems and websites", "tech.g3": "Data and server", "tech.g4": "Integrations",
  "tech.i1": "Payments", "tech.i2": "Maps and location", "tech.i3": "Email and notifications", "tech.i4": "Sign in with Google and Apple",
  "faq.tag": "Questions",
  "faq.h2": "Frequently asked questions.",
  "faq.q1": "How much does a project cost?",
  "faq.a1": "It depends on the scope. After the first conversation you get a written quote with a fixed price and deadline. If the scope doesn't change, the price stays the same.",
  "faq.q2": "How long does it take?",
  "faq.a2": "The timeline depends on the scope and is written in the quote. We work in stages and you see a working version after each one, so you can follow the progress the whole time.",
  "faq.q3": "We only have an idea, no brief. Is that enough?",
  "faq.a3": "Yes. We prepare the brief together during the first conversations and it becomes part of the quote.",
  "faq.q4": "Who publishes the app on the App Store and Google Play?",
  "faq.a4": "We do. We prepare the descriptions and screenshots, submit the app and work with the Apple and Google review teams until it is approved.",
  "faq.q5": "Can you connect the new system to the software we already use?",
  "faq.a5": "In most cases, yes. Before the quote we check what connection options each tool offers and tell you what is possible.",
  "faq.q6": "Do you work with clients remotely?",
  "faq.a6": "Yes. Conversations and reviews of the work happen online, and we meet in person when needed.",
  "faq.q7": "What happens after launch?",
  "faq.a7": "We take over the maintenance: we keep the product running, update it and add new features when you need them. The terms are agreed together with the project.",
})

TAGS = "title|a|span|p|h1|h2|h3|h4|li|div|b|em|dt|dd"


def build():
    s = io.open(SRC, encoding="utf-8").read()
    missing, used = [], set()

    def esc(t):
        return t.replace("&", "&amp;").replace('"', "&quot;")

    # 1) мета тагове: <meta ... data-i18n-attr="content" data-i18n="key" content="...">
    def meta_sub(m):
        tag, key = m.group(0), m.group(1)
        used.add(key)
        if key not in EN:
            missing.append(key); return tag
        return re.sub(r'content="[^"]*"', 'content="%s"' % esc(EN[key]), tag, count=1)
    s = re.sub(r'<meta[^>]*data-i18n-attr="content"[^>]*data-i18n="([^"]+)"[^>]*>', meta_sub, s)

    # 2) текст: <tag ... data-i18n="key" ...>ТЕКСТ</tag>   (без вложени тагове вътре)
    def text_sub(m):
        open_tag, key, close = m.group(1), m.group(2), m.group(4)
        used.add(key)
        if key not in EN:
            missing.append(key); return m.group(0)
        return open_tag + EN[key].replace("&", "&amp;") + close
    s = re.sub(r'(<(?:%s)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)([^<]*)(</(?:%s)>)' % (TAGS, TAGS), text_sub, s)

    # 3) език на документа и бутонът за език
    s = s.replace('<html lang="bg">', '<html lang="en">', 1)
    s = s.replace('<a href="en/" class="lang" id="langSwitch" hreflang="en" lang="en" title="English">EN</a>',
                  '<a href="../" class="lang" id="langSwitch" hreflang="bg" lang="bg" title="Български">BG</a>', 1)

    # търсачки: адресът на страницата, картинката за споделяне и структурираните данни на английски
    HEAD = [
      ('<link rel="canonical" href="https://codemsolution.com/">', '<link rel="canonical" href="https://codemsolution.com/en/">'),
      ('<meta property="og:url" content="https://codemsolution.com/">', '<meta property="og:url" content="https://codemsolution.com/en/">'),
      ('<meta property="og:image" content="https://codemsolution.com/assets/img/og.png">', '<meta property="og:image" content="https://codemsolution.com/assets/img/og-en.png">'),
      ('"legalName": "СИМБИ25 ЕООД"', '"legalName": "SIMBI25 EOOD"'),
      ('"streetAddress": "ул. Ивайло 82", "addressLocality": "Варна"', '"streetAddress": "ul. Ivaylo 82", "addressLocality": "Varna"'),
      ('"name": "България"', '"name": "Bulgaria"'),
      ('["Разработка на софтуер", "Фирмени системи", "Мобилни приложения", "Изработка на сайтове", "Автоматизация на бизнес процеси"]',
       '["Software development", "Business systems", "Mobile apps", "Web development", "Business process automation"]'),
    ]
    for a, bb in HEAD:
        if s.count(a) != 1:
            missing.append("HEAD: " + a[:50])
        s = s.replace(a, bb, 1)
    m = re.search(r'"description": "([^"]*)", "email"', s)
    if m:
        s = s.replace(m.group(0), '"description": "%s", "email"' % EN["meta.desc"], 1)
    else:
        missing.append("HEAD: ld description")

    # страницата с фирмените данни: в EN версията е en/company/
    s = s.replace('href="firma/"', 'href="company/"', 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(s)

    print("en/index.html: %d байта, преведени ключове: %d" % (len(s.encode("utf-8")), len(used)))
    if missing:
        print("ЛИПСВАТ В РЕЧНИКА (останаха на БГ):", sorted(set(missing)))
    unused = sorted(set(EN) - used)
    if unused:
        print("в речника, но не в HTML:", unused)
    visible = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s, flags=re.S)
    left = sorted(set(re.findall(r'[А-Яа-я]{3,}', visible)) - {"Български"})
    if left:
        print("ОСТАНАЛА КИРИЛИЦА:", left[:25])
    dash = [t for t in EN.values() if re.search(r'[—–]| - ', t)]
    if dash:
        print("ТИРЕТА В ПРЕВОДА:", dash)
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(build())
