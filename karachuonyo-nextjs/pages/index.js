import { motion } from "framer-motion";
import { CheckCircle, ArrowRight, MapPin, Phone, Mail, Menu, X, GraduationCap, Heart, Users, Briefcase, Hammer, Shield, Camera, Eye, Play } from "lucide-react";
import { useState } from "react";
import DonateButtons from "../components/DonateButtons";

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
  { 
    title: "Education for All", 
    desc: "Bursaries, ICT labs, and teacher support for every ward.",
    icon: GraduationCap,
    details: "Comprehensive education support including bursary programs, modern ICT laboratories in every school, teacher training and support programs, and infrastructure development for quality learning environments."
  },
  { 
    title: "Healthcare Access", 
    desc: "Equip dispensaries, NHIF sensitization, maternal care access.",
    icon: Heart,
    details: "Fully equipped health dispensaries, NHIF awareness campaigns, improved maternal and child healthcare services, and mobile health clinics for remote areas."
  },
  { 
    title: "Youth Empowerment", 
    desc: "Skills hubs, startup grants, creative economy catalysts.",
    icon: Users,
    details: "Youth skills development centers, startup funding programs, mentorship initiatives, and support for creative industries and digital entrepreneurship."
  },
  { 
    title: "Agriculture & Jobs", 
    desc: "Irrigation, post-harvest storage, farmer co-ops, value chains.",
    icon: Briefcase,
    details: "Modern irrigation systems, post-harvest storage facilities, farmer cooperative support, value addition programs, and market linkage initiatives."
  },
  { 
    title: "Infrastructure & Tech", 
    desc: "Feeder roads, water projects, market sheds, street lighting.",
    icon: Hammer,
    details: "Improved feeder roads, clean water projects, modern market infrastructure, street lighting, and digital connectivity initiatives."
  },
  { 
    title: "Unity & Inclusion", 
    desc: "Open budgets, ward scorecards, community forums quarterly.",
    icon: Shield,
    details: "Transparent governance, regular community forums, inclusive decision-making processes, and accountability mechanisms for all development projects."
  },
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

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [expandedCard, setExpandedCard] = useState(null);
  const [lightboxImage, setLightboxImage] = useState(null);
  
  const scrollTo = (id)=> {
    const el = document.getElementById(id);
    if(el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setMobileMenuOpen(false);
  };

  return (
    <div className="text-center flex">
      {/* Sidebar Navigation */}
      <aside className={`sidebar fixed left-0 top-0 h-screen w-64 bg-white/95 backdrop-blur border-r border-gray-200 z-50 shadow-lg md:translate-x-0 ${mobileMenuOpen ? 'open' : ''}`}>
        <div className="p-6">
          {/* Logo and Title */}
          <div className="flex flex-col items-center justify-center gap-4 mb-8">
            <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-blue-700 to-green-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg text-center">KF</span>
            </div>
            <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-blue-700 to-green-600 bg-clip-text text-transparent text-center">
              Karachuonyo First
            </span>
          </div>
          
          {/* Navigation Menu */}
          <nav className="flex flex-col space-y-2">
            {nav.map(n=> (
              <button 
                key={n.id} 
                onClick={()=>scrollTo(n.id)} 
                className="text-left text-base font-medium hover:text-blue-700 hover:bg-blue-50 transition-all duration-200 py-3 px-4 rounded-lg border-b border-gray-100"
              >
                {n.label}
              </button>
            ))}
            <button onClick={()=>scrollTo('contact')} className="btn bg-blue-600 text-white hover:bg-blue-700 mt-4 w-full">
              Donate Now
            </button>
          </nav>
        </div>
      </aside>
      
      {/* Main Content */}
      <div className="main-content flex-1 ml-64 md:ml-64">
        <header className="sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-4 h-20 flex items-center justify-center relative">
            {/* Mobile Menu Button */}
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden absolute left-4 p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
            <span className="font-extrabold text-2xl tracking-tight bg-gradient-to-r from-blue-700 to-green-600 bg-clip-text text-transparent">
              Welcome to Karachuonyo First
            </span>
          </div>
        </header>

      <section id="home" className="relative overflow-hidden min-h-screen flex items-center">
        {/* Background with overlay */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-blue-800 to-green-700" />
          <div className="absolute inset-0 bg-black/20" />
          {/* Decorative elements */}
          <div className="absolute top-20 left-10 w-32 h-32 bg-white/10 rounded-full blur-xl" />
          <div className="absolute bottom-20 right-10 w-48 h-48 bg-yellow-400/20 rounded-full blur-2xl" />
        </div>
        
        <div className="relative max-w-6xl mx-auto px-4 py-24 md:py-32 text-white z-10">
          <motion.div 
            initial={{opacity:0, y:30}} 
            animate={{opacity:1, y:0}} 
            transition={{duration:0.8}}
            className="text-center md:text-left"
          >
            <motion.h1 
              initial={{opacity:0, y:20}} 
              animate={{opacity:1, y:0}} 
              transition={{duration:0.6, delay:0.2}} 
              className="text-5xl md:text-7xl font-black leading-tight mb-6"
            >
              <span className="block">Karachuonyo First —</span>
              <span className="block text-yellow-400">Putting Our People Ahead</span>
            </motion.h1>
            
            <motion.p 
              initial={{opacity:0, y:20}} 
              animate={{opacity:1, y:0}} 
              transition={{duration:0.6, delay:0.4}}
              className="text-xl md:text-2xl text-white/90 max-w-3xl mb-4 font-medium"
            >
              Education. Development. Unity. Progress.
            </motion.p>
            
            <motion.p 
              initial={{opacity:0, y:20}} 
              animate={{opacity:1, y:0}} 
              transition={{duration:0.6, delay:0.6}}
              className="text-lg text-white/80 max-w-2xl mb-10"
            >
              A people-centered agenda for opportunity, dignity, and shared prosperity across Karachuonyo.
            </motion.p>
            
            <motion.div 
              initial={{opacity:0, y:20}} 
              animate={{opacity:1, y:0}} 
              transition={{duration:0.6, delay:0.8}}
              className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start"
            >
              <button 
                onClick={()=>scrollTo('agenda')} 
                className="btn bg-yellow-400 text-black hover:bg-yellow-300 text-lg px-8 py-4 font-bold shadow-2xl"
              >
                Join the Movement
              </button>
              <button 
                onClick={()=>scrollTo('contact')} 
                className="btn border-2 border-white text-white hover:bg-white hover:text-black text-lg px-8 py-4 font-bold" 
                style={{background:'transparent'}}
              >
                Donate Today <ArrowRight className="inline-block ml-2 h-5 w-5" />
              </button>
            </motion.div>
          </motion.div>
        </div>
        
        {/* Scroll indicator */}
        <motion.div 
          initial={{opacity:0}} 
          animate={{opacity:1}} 
          transition={{duration:1, delay:1.5}}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white/60"
        >
          <div className="flex flex-col items-center">
            <span className="text-sm mb-2">Scroll to explore</span>
            <motion.div 
              animate={{y: [0, 10, 0]}} 
              transition={{duration:2, repeat:Infinity}}
              className="w-6 h-10 border-2 border-white/40 rounded-full flex justify-center"
            >
              <div className="w-1 h-3 bg-white/60 rounded-full mt-2" />
            </motion.div>
          </div>
        </motion.div>
      </section>

      <section id="about" className="bg-white">
        <div className="max-w-6xl mx-auto px-4 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Candidate Photo */}
            <motion.div 
              initial={{opacity:0, x:-30}} 
              whileInView={{opacity:1, x:0}} 
              transition={{duration:0.6}}
              viewport={{once:true}}
              className="relative"
            >
              <div className="aspect-[4/3] rounded-2xl bg-gradient-to-br from-blue-100 via-blue-200 to-green-200 shadow-2xl relative overflow-hidden">
                {/* Candidate card */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    {/* Circle with candidate image */}
                    <div className="w-24 h-24 rounded-full mx-auto mb-4 overflow-hidden shadow-lg">
                      <img
                        src="/candidate_photo.jpg"   // <-- put your image in the public folder
                        alt="Felix Obuya"
                        className="w-full h-full object-cover"
                      />
                    </div>

                    {/* Candidate details */}
                    <p className="text-gray-600 font-medium">Felix Obuya</p>
                    <p className="text-sm text-gray-500">Candidate Photo</p>
                  </div>
                </div>
                {/* Decorative elements */}
                <div className="absolute top-4 right-4 w-16 h-16 bg-yellow-400/30 rounded-full blur-xl" />
                <div className="absolute bottom-4 left-4 w-20 h-20 bg-blue-600/20 rounded-full blur-xl" />
              </div>
            </motion.div>
            
            {/* Content */}
            <motion.div 
              initial={{opacity:0, x:30}} 
              whileInView={{opacity:1, x:0}} 
              transition={{duration:0.6, delay:0.2}}
              viewport={{once:true}}
            >
              <h2 className="text-3xl md:text-4xl font-extrabold mb-6 gradient-text">Meet the Candidate</h2>
              <p className="text-gray-700 text-lg leading-relaxed mb-8">
                I am Felix Obuya—committed to servant leadership that listens first and acts fast. 
                Together, we will unlock opportunities for youth, safeguard health and education, 
                and build Karachuonyo with integrity and transparency.
              </p>
              
              {/* Core Values Grid */}
              <div className="space-y-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Core Values</h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  {[
                    {icon: Shield, title: "Transparency", desc: "Open governance and accountability"},
                    {icon: Users, title: "Community First", desc: "People-centered decision making"},
                    {icon: Heart, title: "Empowering Youth", desc: "Investing in the next generation"},
                    {icon: Hammer, title: "Sustainable Development", desc: "Building for the future"}
                  ].map((value, i) => {
                    const IconComponent = value.icon;
                    return (
                      <motion.div 
                        key={i}
                        initial={{opacity:0, y:20}} 
                        whileInView={{opacity:1, y:0}} 
                        transition={{duration:0.4, delay:0.3 + (i * 0.1)}}
                        viewport={{once:true}}
                        className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 hover:bg-blue-50 transition-colors duration-200"
                      >
                        <div className="flex-shrink-0">
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-green-600 rounded-lg flex items-center justify-center">
                            <IconComponent className="h-5 w-5 text-white" />
                          </div>
                        </div>
                        <div className="text-center">
                          <h4 className="font-bold text-gray-900 mb-1">{value.title}</h4>
                          <p className="text-sm text-gray-600">{value.desc}</p>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section id="agenda" className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <motion.div 
            initial={{opacity:0, y:30}} 
            whileInView={{opacity:1, y:0}} 
            transition={{duration:0.6}}
            viewport={{once:true}}
            className="text-center mb-12"
          >
            <h2 className="text-3xl md:text-4xl font-extrabold mb-4">Our Agenda</h2>
            <p className="text-gray-600 text-lg max-w-3xl mx-auto">
              Six actionable pillars that turn promises into measurable projects for Karachuonyo's development.
            </p>
          </motion.div>
          
          <div className="flex flex-col md:flex-row gap-6 overflow-x-auto">
            {agenda.map((item, index) => {
              const IconComponent = item.icon;
              const isExpanded = expandedCard === index;
              
              return (
                <motion.div 
                  key={index}
                  initial={{opacity:0, y:30}} 
                  whileInView={{opacity:1, y:0}}
                  transition={{duration:0.6, delay:index * 0.1}}
                  viewport={{once:true}}
                  className="card p-6 cursor-pointer transition-all duration-300 flex-shrink-0 w-full md:w-80 lg:w-96"
                  onClick={() => setExpandedCard(isExpanded ? null : index)}
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-green-600 rounded-xl flex items-center justify-center">
                        <IconComponent className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    
                    <div className="flex-1">
                      <h3 className="text-xl font-bold mb-2 text-gray-900">{item.title}</h3>
                      <p className="text-gray-600 mb-3">{item.desc}</p>
                      
                      {isExpanded && (
                        <motion.div 
                          initial={{opacity:0, height:0}} 
                          animate={{opacity:1, height:'auto'}} 
                          exit={{opacity:0, height:0}}
                          transition={{duration:0.3}}
                          className="border-t border-gray-200 pt-4 mt-4"
                        >
                          <p className="text-gray-700 leading-relaxed">{item.details}</p>
                        </motion.div>
                      )}
                      
                      <div className="flex items-center justify-between mt-4">
                        <span className="text-sm font-medium text-blue-600">
                          {isExpanded ? 'Click to collapse' : 'Click to expand'}
                        </span>
                        <motion.div 
                          animate={{rotate: isExpanded ? 180 : 0}}
                          transition={{duration:0.3}}
                        >
                          <ArrowRight className="h-4 w-4 text-blue-600" />
                        </motion.div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      <section id="news" className="max-w-6xl mx-auto px-4 py-16">
        <motion.div 
          initial={{opacity:0, y:30}} 
          whileInView={{opacity:1, y:0}} 
          transition={{duration:0.6}}
          viewport={{once:true}}
          className="flex items-end justify-between gap-4"
        >
          <div>
            <h2 className="text-3xl md:text-4xl font-extrabold">News & Updates</h2>
            <p className="text-gray-600">Campaign milestones, project progress, and statements.</p>
          </div>
        </motion.div>
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          {posts.map((p,i)=> (
            <motion.div 
              key={i} 
              initial={{opacity:0, y:30}} 
              whileInView={{opacity:1, y:0}} 
              transition={{duration:0.6, delay:i * 0.1}}
              viewport={{once:true}}
              whileHover={{y: -5}}
              className="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 group cursor-pointer"
            >
              <div className="h-40 bg-gradient-to-br from-blue-400 to-purple-600 rounded-t-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
                <div className="absolute inset-0 flex items-center justify-center text-white">
                  <div className="text-center">
                    <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-2">
                      <span className="text-lg font-bold">{p.title.charAt(0)}</span>
                    </div>
                    <span className="text-xs opacity-90">Featured News</span>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <div className="text-xs text-blue-600 font-medium">{p.date} • {p.tag}</div>
                <h3 className="font-bold mt-2 group-hover:text-blue-600 transition-colors duration-300">{p.title}</h3>
                <p className="text-gray-600 mt-2">{p.excerpt}</p>
                <motion.button 
                  whileHover={{scale: 1.05}}
                  whileTap={{scale: 0.95}}
                  className="mt-4 btn bg-blue-800 text-white hover:bg-blue-700 flex items-center group-hover:translate-x-1 transition-transform duration-300"
                >
                  Read More <ArrowRight className="w-4 h-4 ml-1" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      <section id="events" className="bg-white">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <motion.h2 
            initial={{opacity:0, y:30}} 
            whileInView={{opacity:1, y:0}} 
            transition={{duration:0.6}}
            viewport={{once:true}}
            className="text-3xl md:text-4xl font-extrabold text-center"
          >
            Upcoming Events
          </motion.h2>
          <div className="mt-10 grid md:grid-cols-3 gap-6">
            {events.map((e,i)=> (
              <motion.div 
                key={i} 
                initial={{opacity:0, y:30}} 
                whileInView={{opacity:1, y:0}}
                transition={{duration:0.6, delay:i * 0.1}}
                viewport={{once:true}}
                whileHover={{y: -3, scale: 1.02}}
                className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-2xl shadow-md hover:shadow-lg transition-all duration-300 group border border-gray-200 hover:border-blue-300"
              >
                <div className="flex items-center mb-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3 group-hover:bg-blue-200 transition-colors duration-300">
                    <MapPin className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="font-semibold text-blue-800 group-hover:text-blue-600 transition-colors duration-300">{e.title}</div>
                    <div className="text-sm text-gray-600">{e.date}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2 mt-2 text-gray-600">
                  <span className="text-sm">{e.place}</span>
                </div>
                <div className="flex items-center justify-between pt-4 border-t border-gray-200 mt-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span className="text-xs text-green-600 font-medium">Upcoming</span>
                  </div>
                  <motion.button 
                    whileHover={{scale: 1.05}}
                    whileTap={{scale: 0.95}}
                    className="btn bg-green-600 text-white hover:bg-green-700 flex items-center group-hover:translate-x-1 transition-transform duration-300"
                  >
                    Attend <ArrowRight className="w-4 h-4 ml-1" />
                  </motion.button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section id="gallery" className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <motion.h2 
            className="text-3xl md:text-4xl font-extrabold mb-6 text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            Gallery
          </motion.h2>
          <motion.div 
            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8, staggerChildren: 0.1 }}
            viewport={{ once: true }}
          >
            {[
              { id: 1, title: "Community Forum - Kendu Bay", category: "Events" },
              { id: 2, title: "Youth Skills Workshop", category: "Education" },
              { id: 3, title: "Healthcare Outreach Program", category: "Healthcare" },
              { id: 4, title: "Agricultural Training Session", category: "Agriculture" },
              { id: 5, title: "Infrastructure Development Visit", category: "Development" },
              { id: 6, title: "Unity Rally - Oyugis", category: "Unity" },
              { id: 7, title: "Clean-up Drive", category: "Environment" },
              { id: 8, title: "Women Empowerment Meeting", category: "Empowerment" }
            ].map((item) => (
              <motion.div 
                key={item.id} 
                className="relative group cursor-pointer overflow-hidden rounded-lg shadow-md hover:shadow-xl transition-all duration-300"
                whileHover={{ scale: 1.05 }}
                onClick={() => setLightboxImage(item)}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: item.id * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="bg-gradient-to-br from-blue-400 to-purple-600 h-64 flex flex-col items-center justify-center text-white relative">
                  <div className="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-all duration-300"></div>
                  <Camera className="w-12 h-12 mb-3 opacity-80" />
                  <span className="text-sm font-medium text-center px-2 relative z-10">{item.title}</span>
                  <span className="text-xs opacity-75 mt-1 relative z-10">{item.category}</span>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="absolute bottom-4 left-4 right-4 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300 opacity-0 group-hover:opacity-100">
                    <div className="flex items-center justify-between text-white">
                      <span className="text-xs">Click to view</span>
                      <Eye className="w-4 h-4" />
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
          
          {/* Video Section */}
          <motion.div 
            className="mt-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h3 className="text-2xl font-bold text-center mb-8 text-gray-800">Campaign Videos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-800 rounded-lg h-64 flex items-center justify-center relative overflow-hidden group cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-red-500 to-red-700"></div>
                <div className="relative z-10 text-center text-white">
                  <Play className="w-16 h-16 mx-auto mb-4 opacity-80 group-hover:opacity-100 transition-opacity" />
                  <p className="font-medium">Campaign Launch Video</p>
                  <p className="text-sm opacity-75">Karachuonyo First Vision</p>
                </div>
              </div>
              <div className="bg-gray-800 rounded-lg h-64 flex items-center justify-center relative overflow-hidden group cursor-pointer">
                <div className="absolute inset-0 bg-gradient-to-br from-green-500 to-green-700"></div>
                <div className="relative z-10 text-center text-white">
                  <Play className="w-16 h-16 mx-auto mb-4 opacity-80 group-hover:opacity-100 transition-opacity" />
                  <p className="font-medium">Community Testimonials</p>
                  <p className="text-sm opacity-75">Voices from Karachuonyo</p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
        
        {/* Lightbox Modal */}
        {lightboxImage && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
            onClick={() => setLightboxImage(null)}
          >
            <div className="relative max-w-4xl max-h-full">
              <button 
                className="absolute top-4 right-4 text-white hover:text-gray-300 z-10"
                onClick={() => setLightboxImage(null)}
              >
                <X className="w-8 h-8" />
              </button>
              <div className="bg-gradient-to-br from-blue-400 to-purple-600 rounded-lg overflow-hidden">
                <div className="h-96 flex flex-col items-center justify-center text-white p-8">
                  <Camera className="w-24 h-24 mb-6 opacity-80" />
                  <h3 className="text-2xl font-bold mb-2">{lightboxImage.title}</h3>
                  <p className="text-lg opacity-90 mb-4">{lightboxImage.category}</p>
                  <p className="text-center opacity-75 max-w-md">
                    This image showcases our commitment to {lightboxImage.category.toLowerCase()} in the Karachuonyo constituency. 
                    Together, we're building a stronger community for everyone.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </section>

      <section className="bg-gradient-to-br from-blue-900 to-green-700 text-white">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <motion.div 
            initial={{opacity:0, y:30}} 
            whileInView={{opacity:1, y:0}} 
            transition={{duration:0.6}}
            viewport={{once:true}}
            className="text-center mb-12"
          >
            <h2 className="text-3xl md:text-4xl font-extrabold mb-4">Get Involved</h2>
            <p className="text-white/90 text-lg max-w-2xl mx-auto">Volunteer, mobilize, and be the reason Karachuonyo rises. Every contribution matters in building our community.</p>
          </motion.div>
          
          <div className="grid lg:grid-cols-2 gap-12 items-start">
            {/* Volunteer Form */}
            <motion.div 
              initial={{opacity:0, x:-30}} 
              whileInView={{opacity:1, x:0}} 
              transition={{duration:0.6, delay:0.2}}
              viewport={{once:true}}
              className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20"
            >
              <h3 className="text-xl font-bold mb-6 flex items-center">
                <Users className="w-6 h-6 mr-3" />
                Join Our Team
              </h3>
              <form action="/api/form-submit" method="post" onSubmit={(e)=>{ e.preventDefault(); fetch('/api/form-submit',{method:'POST', body: JSON.stringify({ name: e.target.name.value, email: e.target.email.value, phone: e.target.phone.value, role: e.target.role.value, message: e.target.message.value, target: 'volunteer' }), headers: {'Content-Type':'application/json'}}).then(()=> alert('Thanks for joining us!')).catch(()=> alert('Error submitting form')) }} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-white/90 mb-2">Full Name</label>
                    <input 
                      name="name" 
                      placeholder="Enter your full name" 
                      className="w-full p-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:bg-white/30 focus:border-white/50 transition-all duration-300" 
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/90 mb-2">Email Address</label>
                    <input 
                      name="email" 
                      type="email" 
                      placeholder="your.email@example.com" 
                      className="w-full p-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:bg-white/30 focus:border-white/50 transition-all duration-300" 
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">Phone Number</label>
                  <input 
                    name="phone" 
                    placeholder="+254 700 000 000" 
                    className="w-full p-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:bg-white/30 focus:border-white/50 transition-all duration-300" 
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">How would you like to help?</label>
                  <select 
                    name="role" 
                    className="w-full p-3 rounded-lg bg-white/20 border border-white/30 text-white focus:bg-white/30 focus:border-white/50 transition-all duration-300"
                    required
                  >
                    <option value="" className="text-gray-800">Select an option</option>
                    <option value="volunteer" className="text-gray-800">General Volunteer</option>
                    <option value="campaign-ambassador" className="text-gray-800">Campaign Ambassador</option>
                    <option value="event-organizer" className="text-gray-800">Event Organizer</option>
                    <option value="social-media" className="text-gray-800">Social Media Support</option>
                    <option value="fundraising" className="text-gray-800">Fundraising</option>
                    <option value="youth-coordinator" className="text-gray-800">Youth Coordinator</option>
                    <option value="community-outreach" className="text-gray-800">Community Outreach</option>
                    <option value="other" className="text-gray-800">Other</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/90 mb-2">Tell us more about yourself</label>
                  <textarea 
                    name="message" 
                    placeholder="Share your skills, experience, or why you want to join our movement..." 
                    rows="4" 
                    className="w-full p-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:bg-white/30 focus:border-white/50 transition-all duration-300 resize-none"
                  ></textarea>
                </div>
                
                <div className="flex items-center">
                  <input type="checkbox" id="newsletter" className="mr-3 w-4 h-4 text-blue-600 bg-white/20 border-white/30 rounded" />
                  <label htmlFor="newsletter" className="text-sm text-white/80">
                    Subscribe to our newsletter for campaign updates
                  </label>
                </div>
                
                <motion.button 
                  type="submit" 
                  className="btn bg-white text-blue-900 hover:bg-white/90 w-full font-bold py-3 shadow-lg"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Join the Movement
                </motion.button>
              </form>
            </motion.div>
            
            {/* Ways to Help */}
            <motion.div 
              initial={{opacity:0, x:30}} 
              whileInView={{opacity:1, x:0}} 
              transition={{duration:0.6, delay:0.4}}
              viewport={{once:true}}
              className="space-y-6"
            >
              <h3 className="text-2xl font-bold mb-6">Ways to Make a Difference</h3>
              
              <div className="space-y-4">
                {[
                  {
                    icon: Users,
                    title: "Volunteer",
                    description: "Join our ground team and help with community outreach, event organization, and voter education."
                  },
                  {
                    icon: Heart,
                    title: "Donate",
                    description: "Support our campaign financially to help us reach more communities and amplify our message."
                  },
                  {
                    icon: Shield,
                    title: "Advocate",
                    description: "Become a campaign ambassador and help spread our vision within your networks and community."
                  },
                  {
                    icon: GraduationCap,
                    title: "Educate",
                    description: "Help educate voters about our policies and the importance of participating in the democratic process."
                  }
                ].map((item, index) => {
                  const IconComponent = item.icon;
                  return (
                    <motion.div 
                      key={index}
                      className="flex items-start space-x-4 p-4 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 hover:bg-white/20 transition-all duration-300"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.6 + (index * 0.1) }}
                      viewport={{ once: true }}
                    >
                      <div className="flex-shrink-0">
                        <IconComponent className="w-8 h-8 text-yellow-400" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                        <p className="text-white/80 text-sm">{item.description}</p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
              
              <div className="bg-white/20 backdrop-blur-sm p-6 rounded-lg border border-white/30">
                <h4 className="font-bold text-lg mb-2">Ready to Get Started?</h4>
                <p className="text-white/90 mb-4">Every contribution matters, no matter how small. Together, we can build a better Karachuonyo.</p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <button 
                    onClick={()=>scrollTo('contact')} 
                    className="flex-1 bg-white/20 border border-white/30 text-white py-2 px-4 rounded-lg font-semibold hover:bg-white/30 transition-all duration-300"
                  >
                    Contact Us
                  </button>
                  <button 
                    onClick={()=>scrollTo('agenda')} 
                    className="flex-1 bg-yellow-400 text-blue-900 py-2 px-4 rounded-lg font-semibold hover:bg-yellow-300 transition-all duration-300"
                  >
                    Learn More
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 py-16">
        <motion.div 
          className="rounded-2xl border p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-6 bg-gradient-to-r from-blue-50 to-green-50 border-blue-200 shadow-lg hover:shadow-xl transition-all duration-300"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <h3 className="text-2xl font-bold text-gray-800">Stay in the loop</h3>
            <p className="text-gray-600">Get weekly updates from the campaign trail and policy developments.</p>
          </motion.div>
          <motion.div 
            className="flex w-full md:w-auto gap-3"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
          >
            <input 
              placeholder="Enter your email" 
              className="p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300 flex-1 min-w-[250px]" 
            />
            <button className="btn bg-blue-800 text-white hover:bg-blue-900 px-6 py-3 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
              Subscribe
            </button>
          </motion.div>
        </motion.div>
      </section>

      <section id="contact" className="bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-6xl mx-auto px-4 py-16 grid md:grid-cols-2 gap-10">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <motion.h2 
              className="text-3xl md:text-4xl font-extrabold mb-3 bg-gradient-to-r from-blue-800 to-green-600 bg-clip-text text-transparent"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              Contact
            </motion.h2>
            <motion.p 
              className="text-gray-600 mb-6"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              viewport={{ once: true }}
            >
              We're here for your ideas and feedback. Reach out any time.
            </motion.p>
            <motion.div 
              className="space-y-4 text-sm"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              viewport={{ once: true }}
            >
              <motion.div 
                className="flex items-center gap-3 p-3 bg-white/70 backdrop-blur-sm rounded-lg hover:bg-white/90 transition-all duration-300"
                whileHover={{ scale: 1.02 }}
              >
                <Phone className="h-5 w-5 text-blue-600"/> 
                <span className="font-medium">0700 686 943</span>
              </motion.div>
              <motion.div 
                className="flex items-center gap-3 p-3 bg-white/70 backdrop-blur-sm rounded-lg hover:bg-white/90 transition-all duration-300"
                whileHover={{ scale: 1.02 }}
              >
                <Mail className="h-5 w-5 text-blue-600"/> 
                <span className="font-medium">obuyafelixm@gmail.com</span>
              </motion.div>
              <motion.div 
                className="flex items-center gap-3 p-3 bg-white/70 backdrop-blur-sm rounded-lg hover:bg-white/90 transition-all duration-300"
                whileHover={{ scale: 1.02 }}
              >
                <MapPin className="h-5 w-5 text-blue-600"/> 
                <span className="font-medium">South B, Nairobi, Kenya</span>
              </motion.div>
            </motion.div>
            <motion.div 
              className="mt-8"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              viewport={{ once: true }}
            >
              <DonateButtons />
            </motion.div>
          </motion.div>
          <motion.div 
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <motion.h3 
              className="font-bold mb-4 text-xl text-gray-800"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              viewport={{ once: true }}
            >
              Send a Message
            </motion.h3>
            <motion.form 
              action="/api/form-submit" 
              method="post" 
              onSubmit={(e)=>{ e.preventDefault(); fetch('/api/form-submit',{method:'POST', body: JSON.stringify({ name: e.target.fname.value + ' ' + e.target.lname.value, email: e.target.email.value, phone: '', message: e.target.message.value, target: 'contact' }), headers: {'Content-Type':'application/json'}}).then(()=> alert('Message sent successfully!')).catch(()=> alert('Error sending message'))}}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              viewport={{ once: true }}
            >
              <div className="grid md:grid-cols-2 gap-3 mb-4">
                <input 
                  name="fname" 
                  placeholder="First name" 
                  className="p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300" 
                  required
                />
                <input 
                  name="lname" 
                  placeholder="Last name" 
                  className="p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300" 
                  required
                />
              </div>
              <input 
                name="email" 
                type="email" 
                placeholder="Email" 
                className="w-full p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300 mb-4" 
                required
              />
              <textarea 
                name="message" 
                placeholder="Your message" 
                rows="5" 
                className="w-full p-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300 mb-4 resize-none" 
                required
              ></textarea>
              <motion.button 
                type="submit" 
                className="btn bg-blue-800 text-white w-full py-3 rounded-lg font-semibold shadow-md hover:shadow-lg hover:bg-blue-900 transition-all duration-300 transform hover:scale-105"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Send Message
              </motion.button>
            </motion.form>
          </motion.div>
        </div>
      </section>

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
              {nav.map(n=> <li key={n.id}><button onClick={()=>scrollTo(n.id)} className="hover:text-white">{n.label}</button></li>)}
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Connect</h4>
            <div className="flex gap-3">
              <a className="inline-flex items-center justify-center h-10 w-10 rounded-full bg-white/10">F</a>
              <a className="inline-flex items-center justify-center h-10 w-10 rounded-full bg-white/10">T</a>
              <a className="inline-flex items-center justify-center h-10 w-10 rounded-full bg-white/10">I</a>
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
    </div>
  );
}
