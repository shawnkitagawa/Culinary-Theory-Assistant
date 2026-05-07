// import culinary_feature_1 from "../../public/culinary_feature_1.jpg"
// import culinary_feature_2 from "../../public/culinary_feature_2.jpg"
// import culinary_feature_3 from "../../public/culinary_feature_3.jpg"
// export function FeatureSection() {



//     return (
//         <section className="bg-neutral-700 px-8 py-16 md:px-12">

//             <p className="mb-8 text-[10px] font-medium uppercase tracking-[0.28em] text-neutral-400">
//                 Engineered for culinary precision
//             </p>

//             <div className="mb-16 grid grid-cols-[0.7fr_1fr] items-end gap-12">
//                 <h1 className="text-4xl font-bold leading-[1.04] tracking-[-0.03em] text-neutral-50 sm:text-5xl lg:text-[3.25rem]">
//                     AI-powered
//                     <br />
//                     answers.
//                     <br />
//                     Real culinary
//                     <br />
//                     expertise.
//                 </h1>
//                 <p className="max-w-sm self-end text-sm leading-relaxed text-neutral-400">
//                     Learn cooking techniques with AI answers backed by real culinary knowledge.
//                 </p>
//             </div>

//             <div className="grid gap-4 md:grid-cols-3">
//                 {[
//                     { img: culinary_feature_1, tag: "Sources", title: "Verified answers from real sources", body: "Responses grounded in professional culinary documents for reliable, precise technique guidance." },
//                     { img: culinary_feature_2, tag: "Workflow", title: "Flexible for every kitchen workflow", body: "Explore techniques, develop recipes, and generate creative ideas based on your goals and ingredients." },
//                     { img: culinary_feature_3, tag: "Architecture", title: "Built on a modern full-stack system", body: "Reliable answers and smooth performance through advanced retrieval and AI architecture." },
//                 ].map(({ img, tag, title, body }) => (
//                     <div key={tag} className="flex flex-col rounded-[20px] border border-white/10 bg-white/5 p-5">
//                         <img
//                             src={img}
//                             className="mb-5 h-48 w-full rounded-2xl object-cover"
//                             alt={title}
//                         />
//                         <div className="mb-3 flex items-center gap-1.5">
//                             <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
//                             <span className="text-[10px] font-medium uppercase tracking-[0.2em] text-neutral-400">{tag}</span>
//                         </div>
//                         <h2 className="mb-2 text-base font-medium leading-snug tracking-tight text-neutral-50">
//                             {title}
//                         </h2>
//                         <p className="text-[13px] leading-relaxed text-neutral-400">{body}</p>
//                     </div>
//                 ))}
//             </div>

//         </section>
//     );
// }
import { motion } from "framer-motion";

interface Feature {
    icon: string;
    title: string;
    description: string;
    accent: string;
}

const FEATURES: Feature[] = [
    {
        icon: "📚",
        title: "Source-Aware Answers",
        description:
            "Every response cites exact passages from trusted culinary texts — On Food and Cooking, Modernist Cuisine, and more.",
        accent: "#c8963c",
    },
    {
        icon: "🔬",
        title: "Theory-Backed Science",
        description:
            "Understand the chemistry and physics behind every technique. Why does bread proof? Why does fat carry flavour?",
        accent: "#a0522d",
    },
    {
        icon: "🎯",
        title: "Technique Precision",
        description:
            "Sautéing vs. sweating. Braising vs. stewing. Nuances that matter to serious cooks, explained clearly.",
        accent: "#8a9e78",
    },
    {
        icon: "⚙️",
        title: "RAG Pipeline",
        description:
            "Semantic embeddings retrieve the most relevant knowledge chunks before generation — grounded in real content.",
        accent: "#6b8fa0",
    },
    {
        icon: "🌐",
        title: "Multilingual Support",
        description:
            "Get theory-backed answers in English or Japanese. Auto-detect mode matches the language of your question.",
        accent: "#9b7ec8",
    },
    {
        icon: "🍽️",
        title: "Built for Professionals",
        description:
            "Designed for culinary students, line cooks, private chefs, recipe developers, and serious home cooks.",
        accent: "#c86060",
    },
];

const cardVariants = {
    hidden: {
        opacity: 0,
        y: 60,
        scale: 0.94,
    },
    visible: (index: number) => ({
        opacity: 1,
        y: 0,
        scale: 1,
        transition: {
            delay: index * 0.12,
            duration: 0.7,
            ease: [0.22, 1, 0.36, 1],
        },
    }),
};

const FeatureCard = ({
    feature,
    index,
}: {
    feature: Feature;
    index: number;
}) => {
    return (
        <motion.div
            custom={index}
            variants={cardVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.25 }}
            whileHover={{
                y: -8,
                scale: 1.02,
                transition: { duration: 0.25 },
            }}
            className="group relative overflow-hidden rounded-3xl border border-[#a082641f] bg-white p-7 shadow-[0_8px_32px_rgba(60,40,20,0.06)]"
        >
            <motion.div
                className="absolute left-0 right-0 top-0 h-[2px]"
                style={{
                    background: `linear-gradient(90deg, ${feature.accent}, transparent)`,
                }}
                initial={{ opacity: 0.4 }}
                whileHover={{ opacity: 1 }}
            />

            <div
                className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl text-[22px]"
                style={{ backgroundColor: `${feature.accent}18` }}
            >
                {feature.icon}
            </div>

            <h3 className="mb-2 text-sm font-semibold tracking-wide text-[#1a1612]">
                {feature.title}
            </h3>

            <p className="text-xs font-light leading-relaxed text-[#6b5e54]">
                {feature.description}
            </p>

            <div
                className="pointer-events-none absolute -right-10 -top-10 h-28 w-28 rounded-full opacity-0 blur-2xl transition-opacity duration-300 group-hover:opacity-20"
                style={{ backgroundColor: feature.accent }}
            />
        </motion.div>
    );
};

const GrainOverlay = () => {
    return (
        <div
            className="pointer-events-none absolute inset-0 opacity-[0.028]"
            style={{
                backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
                backgroundRepeat: "repeat",
                backgroundSize: "180px",
            }}
        />
    );
};

export default function FeatureSection() {
    return (
        <section className="relative overflow-hidden bg-[#faf8f3] px-6 py-24 md:px-12 lg:px-[72px]">
            <GrainOverlay />

            <motion.div
                className="pointer-events-none absolute left-1/4 top-1/3 h-[340px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full"
                style={{
                    background:
                        "radial-gradient(ellipse, rgba(200,150,60,0.10) 0%, transparent 70%)",
                }}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1 }}
                viewport={{ once: true }}
            />

            <div className="relative z-10 mx-auto flex max-w-7xl flex-col items-start gap-16 lg:flex-row lg:items-center">
                {/* LEFT */}
                <div className="max-w-xl lg:w-[380px] lg:flex-none">
                    <motion.p
                        className="mb-3 text-xs font-medium uppercase tracking-[0.2em] text-[#c8963c]"
                        initial={{ opacity: 0, y: 12 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.55 }}
                        viewport={{ once: true }}
                    >
                        Why Culinary AI
                    </motion.p>

                    <motion.div
                        className="mb-5 h-[2px] rounded-full bg-gradient-to-r from-[#c8963c] to-[#f5d08a]"
                        initial={{ width: 0 }}
                        whileInView={{ width: 56 }}
                        transition={{ duration: 0.6, delay: 0.1 }}
                        viewport={{ once: true }}
                    />

                    <div className="mb-4 font-serif text-4xl font-light leading-tight text-[#1a1612] md:text-5xl lg:text-[52px]">
                        <motion.div
                            initial={{ opacity: 0, y: 28 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                            viewport={{ once: true }}
                        >
                            Intelligence grounded in
                        </motion.div>

                        <motion.div
                            className="italic text-[#c8963c]"
                            initial={{ opacity: 0, y: 28 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{
                                duration: 0.7,
                                delay: 0.12,
                                ease: [0.22, 1, 0.36, 1],
                            }}
                            viewport={{ once: true }}
                        >
                            culinary science
                        </motion.div>
                    </div>

                    <motion.p
                        className="max-w-md text-[15px] font-light leading-relaxed text-[#6b5e54]"
                        initial={{ opacity: 0, y: 16 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.65, delay: 0.25 }}
                        viewport={{ once: true }}
                    >
                        Every answer is retrieved from a curated knowledge base of trusted
                        culinary texts — not hallucinated from thin air.
                    </motion.p>

                    <motion.button
                        className="mt-8 inline-flex items-center gap-2 rounded-xl bg-[#1a1612] px-6 py-3 text-sm font-medium tracking-wide text-[#faf8f3] shadow-lg transition hover:bg-[#2b241d]"
                        initial={{ opacity: 0, y: 14 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.35 }}
                        viewport={{ once: true }}
                        whileHover={{ scale: 1.04 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        Try the Assistant
                        <span className="text-base">→</span>
                    </motion.button>
                </div>

                {/* RIGHT */}
                <div className="grid w-full flex-1 grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-2">
                    {FEATURES.map((feature, index) => (
                        <FeatureCard key={feature.title} feature={feature} index={index} />
                    ))}
                </div>
            </div>
        </section>
    );
}