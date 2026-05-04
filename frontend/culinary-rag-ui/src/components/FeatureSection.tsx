import culinary_feature_1 from "../../public/culinary_feature_1.jpg"
import culinary_feature_2 from "../../public/culinary_feature_2.jpg"
import culinary_feature_3 from "../../public/culinary_feature_3.jpg"
export function FeatureSection() {



    return (
        <section className="min-h-1/2 bg-neutral-50 px-8 py-15 md:px-12">
            {/* Small label */}
            <p className="text-[10px] uppercase tracking-tight text-neutral-500">
                Engineered for culinary precision
            </p>

            {/* Hero text */}
            <div className="mb-10 ms-11 grid grid-cols-[0.8fr_1fr] items-end gap-6 md:grid-cols-[0.65fr_1fr] md:gap-16">
                <h1 className="text-3xl font-bold leading-[1.05] tracking-tight text-black sm:text-4xl md:text-5xl lg:text-6xl">
                    AI-powered
                    <br />
                    answers.
                    <br />
                    Real culinary
                    <br />
                    expertise.
                </h1>

                <p className="max-w-xl self-end translate-y-6 text-[10px] leading-4 text-neutral-600 md:text-base ">
                    Learn cooking techniques with AI answers backed by real culinary knowledge.
                </p>
            </div>

            {/* Feature cards */}
            <div className="mt-20 grid gap-6 md:grid-cols-3 ">
                <div className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
                    <img src={culinary_feature_1} className="mb-6 h-48 rounded-2xl bg-neutral-100 mx-auto w-full object-cover"></img>

                    <h2 className="text-xl font-medium tracking-tight text-neutral-950">
                        Verified answers from real sources
                    </h2>

                    <p className="mt-4 text-sm leading-6 text-neutral-600">
                        Receive responses grounded in professional culinary documents for
                        reliable, precise technique guidance.
                    </p>
                </div>

                <div className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
                    <img src={culinary_feature_2} className="mb-6 h-48 rounded-2xl bg-neutral-100 mx-auto w-full object-cover"></img>

                    <h2 className="text-xl font-medium tracking-tight text-neutral-950">
                        Flexible for every kitchen workflow
                    </h2>

                    <p className="mt-4 text-sm leading-6 text-neutral-600">
                        Explore techniques, develop recipes, and generate creative culinary
                        ideas based on your goals and ingredients.
                    </p>
                </div>

                <div className="rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm">
                    <img src={culinary_feature_3} className="mb-6 h-48 rounded-2xl bg-neutral-100 mx-auto w-full object-cover"></img>

                    <h2 className="text-xl font-medium tracking-tight text-neutral-950">
                        Built on a modern full-stack system
                    </h2>

                    <p className="mt-4 text-sm leading-6 text-neutral-600">
                        Designed for reliable answers, smooth performance, and future
                        improvements through advanced retrieval and AI architecture.
                    </p>
                </div>
            </div>
        </section>
    );
}