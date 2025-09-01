import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Mail, Phone, MapPin, Facebook, Instagram, Twitter, Youtube, CheckCircle, ArrowRight } from "lucide-react";

export default function CampaignWebsite() {
  const nav = [
    { label: "Home", id: "home" },
    { label: "About", id: "about" },
    { label: "Agenda", id: "agenda" },
    { label: "News", id: "news" },
    { label: "Events", id: "events" },
    { label: "Gallery", id: "gallery" },
    { label: "Contact", id: "contact" },
  ];

  const agenda = [
    { title: "Education", desc: "Bursaries, ICT labs, and teacher support for every ward." },
    { title: "Healthcare", desc: "Equip dispensaries, NHIF sensitization, maternal care access." },
    { title: "Youth & Jobs", desc: "Skills hubs, startup grants, creative economy catalysts." },
    { title: "Infrastructure", desc: "Feeder roads, water projects, market sheds, street lighting." },
    { title: "Agriculture", desc: "Irrigation, post-harvest storage, farmer co-ops, value chains." },
    { title: "Integrity", desc: "Open budgets, ward scorecards, community forums quarterly." },
  ];

  const posts = [
    { title: "Ward Clean-Up Drive Launched", date: "Aug 24, 2025", excerpt: "We flagged off a community clean-up across trading centers with youth groups and churches.", tag: "Community" },
    { title: "Bursary Vetting Guidelines", date: "Aug 18, 2025", excerpt: "Transparent criteria and timelines to ensure fairness and inclusion.", tag: "Education" },
    { title: "Water for Nyadhi – Project Update", date: "Aug 02, 2025", excerpt: "Borehole survey completed; rig mobilization scheduled pending NEMA greenlight.", tag: "Development" },
  ];

  const events = [
    { date: "Sep 05, 2025", title: "Town Hall – Kendu Bay", place: "Kendu Bay Market Hall" },
    { date: "Sep 12, 2025", title: "Youth Skills Clinic", place: "Homa Hills Vocational Center" },
    { date: "Sep 19, 2025", title: "Health Outreach", place: "Kadel Dispensary Grounds" },
  ];

  const socials = [
    { Icon: Facebook, href: "#" },
    { Icon: Twitter, href: "#" },
    { Icon: Instagram, href: "#" },
    { Icon: Youtube, href: "#" },
  ];

  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="font-sans text-gray-800">
      {/* Navbar */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur border-b">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-2xl bg-gradient-to-br from-blue-700 to-green-600" />
            <span className="font-extrabold tracking-tight">Karachuonyo First</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            {nav.map((n) => (
              <button key={n.id} onClick={() => scrollTo(n.id)} className="text-sm hover:text-blue-700">
                {n.label}
              </button>
            ))}
            <Button onClick={() => scrollTo("contact")} className="rounded-2xl">Join the Movement</Button>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section id="home" className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-900 via-blue-800 to-green-700" />
        <svg className="absolute -bottom-16 left-0 opacity-30" width="800" height="300" viewBox="0 0 800 300"><circle cx="200" cy="200" r="200" fill="white"/></svg>
        <div className="relative max-w-6xl mx-auto px-4 py-24 md:py-32 text-white">
          <motion.h1 initial={{opacity:0, y:20}} animate={{opacity:1, y:0}} transition={{duration:0.6}} className="text-5xl md:text-6xl font-black leading-tight">
            Putting Our People Ahead
          </motion.h1>
          <p className="mt-4 md:text-xl text-white/90 max-w-2xl">
            A people-centered agenda for opportunity, dignity, and shared prosperity across Karachuonyo.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button onClick={() => scrollTo("agenda")} className="rounded-2xl">Explore Agenda</Button>
            <Button variant="outline" onClick={() => scrollTo("contact")} className="rounded-2xl border-white text-white hover:text-blue-900 hover:bg-white">
              Volunteer <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="max-w-6xl mx-auto px-4 py-16 grid md:grid-cols-2 gap-10 items-center">
        <div className="aspect-[4/3] rounded-2xl bg-gradient-to-br from-gray-200 to-gray-300 shadow-inner" />
        <div>
          <h2 className="text-3xl md:text-4xl font-extrabold mb-4">Meet the Candidate</h2>
          <p className="text-gray-600">
            I am Felix Obuya—committed to servant leadership that listens first and acts fast. We will unlock opportunities for youth, safeguard health and education, and build with integrity.
          </p>
          <ul className="mt-6 grid sm:grid-cols-2 gap-3">
            {["Community-first decisions","Transparent use of funds","Partnerships over politics","Opportunities for every ward"].map((t,i)=> (
              <li key={i} className="flex items-start gap-2"><CheckCircle className="h-5 w-5 text-green-600 mt-0.5"/><span>{t}</span></li>
            ))}
          </ul>
        </div>
      </section>

      {/* Agenda */}
      <section id="agenda" className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-3xl md:text-4xl font-extrabold text-center">Our Agenda</h2>
          <p className="text-center text-gray-600 mt-2 max-w-2xl mx-auto">Six actionable pillars that turn promises into measurable projects.</p>
          <div className="grid md:grid-cols-3 gap-6 mt-10">
            {agenda.map((a, i) => (
              <Card key={i} className="rounded-2xl">
                <CardHeader>
                  <CardTitle>{a.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-gray-600">{a.desc}</CardContent>
                <CardFooter>
                  <Badge variant="secondary">Q1–Q4 Roadmap</Badge>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* News */}
      <section id="news" className="max-w-6xl mx-auto px-4 py-16">
        <div className="flex items-end justify-between gap-4">
          <div>
            <h2 className="text-3xl md:text-4xl font-extrabold">News & Updates</h2>
            <p className="text-gray-600">Campaign milestones, project progress, and statements.</p>
          </div>
          <Button variant="outline" className="rounded-2xl">View All</Button>
        </div>
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          {posts.map((p, i) => (
            <Card key={i} className="rounded-2xl h-full">
              <div className="h-40 bg-gray-200 rounded-t-2xl" />
              <CardHeader className="space-y-1">
                <Badge className="w-fit">{p.tag}</Badge>
                <CardTitle className="leading-snug">{p.title}</CardTitle>
                <span className="text-xs text-gray-500">{p.date}</span>
              </CardHeader>
              <CardContent className="text-gray-600">{p.excerpt}</CardContent>
              <CardFooter>
                <Button variant="ghost" className="rounded-2xl">Read More</Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </section>

      {/* Events */}
      <section id="events" className="bg-white">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-3xl md:text-4xl font-extrabold text-center">Upcoming Events</h2>
          <div className="mt-10 grid md:grid-cols-3 gap-6">
            {events.map((e, i) => (
              <Card key={i} className="rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-blue-800">{e.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-gray-600 space-y-1">
                  <div className="font-semibold">{e.date}</div>
                  <div className="flex items-center gap-2"><MapPin className="h-4 w-4" />{e.place}</div>
                </CardContent>
                <CardFooter>
                  <Button className="rounded-2xl">Attend</Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Gallery */}
      <section id="gallery" className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-6 text-center">Gallery</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="aspect-square rounded-2xl bg-gradient-to-br from-gray-200 to-gray-300" />
            ))}
          </div>
        </div>
      </section>

      {/* Get Involved / Volunteer */}
      <section className="bg-gradient-to-br from-blue-900 to-green-700 text-white">
        <div className="max-w-6xl mx-auto px-4 py-16 grid md:grid-cols-2 gap-10 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-extrabold">Get Involved</h2>
            <p className="text-white/90 mt-2">Volunteer, mobilize, and be the reason Karachuonyo rises. We’ll get back to you within 48 hours.</p>
            <div className="mt-6 flex flex-wrap gap-3">
              {socials.map(({Icon, href}, i) => (
                <a key={i} href={href} className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 px-3 py-2 rounded-2xl">
                  <Icon className="h-4 w-4" />
                  <span className="text-sm">Follow</span>
                </a>
              ))}
            </div>
          </div>
          <Card className="rounded-2xl border-white/20">
            <CardHeader>
              <CardTitle>Volunteer Form</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Input placeholder="Full Name" />
              <Input placeholder="Email" type="email" />
              <Input placeholder="Phone" />
              <Textarea placeholder="How would you like to help?" rows={4} />
            </CardContent>
            <CardFooter>
              <Button className="w-full rounded-2xl">Submit</Button>
            </CardFooter>
          </Card>
        </div>
      </section>

      {/* Newsletter */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <div className="rounded-2xl border p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-2xl font-bold">Stay in the loop</h3>
            <p className="text-gray-600">Get weekly updates from the campaign.</p>
          </div>
          <div className="flex w-full md:w-auto gap-3">
            <Input placeholder="Enter your email" className="md:w-80" />
            <Button className="rounded-2xl">Subscribe</Button>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section id="contact" className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-16 grid md:grid-cols-2 gap-10">
          <div>
            <h2 className="text-3xl md:text-4xl font-extrabold mb-3">Contact</h2>
            <p className="text-gray-600">We’re here for your ideas and feedback. Reach out any time.</p>
            <div className="mt-6 space-y-3 text-sm">
              <div className="flex items-center gap-2"><Phone className="h-4 w-4"/> 0700 686 943</div>
              <div className="flex items-center gap-2"><Mail className="h-4 w-4"/> obuyafelixm@gmail.com</div>
              <div className="flex items-center gap-2"><MapPin className="h-4 w-4"/> South B, Nairobi, Kenya</div>
            </div>
          </div>
          <Card className="rounded-2xl">
            <CardHeader>
              <CardTitle>Send a Message</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid md:grid-cols-2 gap-3">
                <Input placeholder="First name" />
                <Input placeholder="Last name" />
              </div>
              <Input placeholder="Email" type="email" />
              <Textarea placeholder="Your message" rows={5} />
            </CardContent>
            <CardFooter>
              <Button className="rounded-2xl">Send</Button>
            </CardFooter>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-6xl mx-auto px-4 py-10 grid md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-2xl bg-gradient-to-br from-blue-700 to-green-600" />
              <span className="font-extrabold tracking-tight">Karachuonyo First</span>
            </div>
            <p className="text-white/70 mt-3 text-sm">A movement for dignity, opportunity, and development across all wards.</p>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Quick Links</h4>
            <ul className="space-y-2 text-white/80 text-sm">
              {nav.map((n)=>(
                <li key={n.id}><button onClick={()=>scrollTo(n.id)} className="hover:text-white">{n.label}</button></li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Connect</h4>
            <div className="flex gap-3">
              {socials.map(({Icon, href}, i)=> (
                <a key={i} href={href} className="inline-flex items-center justify-center h-10 w-10 rounded-full bg-white/10 hover:bg-white/20"><Icon className="h-5 w-5"/></a>
              ))}
            </div>
          </div>
        </div>
        <div className="border-t border-white/10">
          <div className="max-w-6xl mx-auto px-4 py-6 text-xs text-white/60 flex flex-col md:flex-row items-center justify-between gap-2">
            <span>© {new Date().getFullYear()} Karachuonyo First. All rights reserved.</span>
            <span>Built with love for Karachuonyo.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
