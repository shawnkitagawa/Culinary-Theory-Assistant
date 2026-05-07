

export function FeatureSectionTeaser() {


    return (
        <section className="bg-neutral-50 px-6 py-20">
            <div className="mx-auto mb-14 max-w-xl text-center">
                <div className="mb-6 inline-flex items-center gap-1.5 rounded-full border border-neutral-200 bg-white px-4 py-1.5">
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                    <span className="text-[10px] font-medium uppercase tracking-[0.28em] text-neutral-500">Coming soon</span>
                </div>
                <h1 className="text-5xl font-bold leading-[1.04] tracking-[-0.03em] text-neutral-950 md:text-6xl">
                    Culinary AI 2.0
                </h1>
                <p className="mt-4 text-base leading-relaxed text-neutral-500">
                    Smarter answers, clearer sources, easier culinary research.
                </p>
            </div>

            <div className="mx-auto max-w-4xl space-y-2.5">
                {/* Row 1 */}
                <div className="grid grid-cols-[2fr_1fr] gap-2.5">
                    <Card icon="ti-bulb" title="Better Questions">
                        2.0 improves how the system understands user intent, expands vague questions,
                        and finds more relevant culinary knowledge before generating an answer.
                    </Card>
                    <Card icon="ti-shield-check" title="More Reliable Answers">
                        Responses will stay closer to trusted culinary knowledge, reducing hallucinations.
                    </Card>
                </div>

                {/* Row 2 */}
                <div className="grid grid-cols-[1fr_2fr] gap-2.5">
                    <Card icon="ti-books" title="Clearer Sources">
                        See exactly where each answer came from, at a glance.
                    </Card>
                    {/* Dark accent card */}
                    <div className="relative overflow-hidden rounded-2xl border border-neutral-800 bg-neutral-950 p-7">
                        <div className="absolute -bottom-10 -right-10 h-40 w-40 rounded-full bg-amber-400/10 blur-2xl" />
                        <div className="relative">
                            <div className="mb-5 flex h-9 w-9 items-center justify-center rounded-xl border border-amber-400/30 bg-amber-400/10">
                                <i className="ti ti-vector-triangle text-lg text-amber-400" aria-hidden />
                            </div>
                            <h2 className="mb-2 text-lg font-medium tracking-tight text-neutral-50">
                                Search That Understands Meaning
                            </h2>
                            <p className="max-w-sm text-[13px] leading-relaxed text-neutral-400">
                                Finds relevant culinary knowledge based on meaning, not just exact keywords —
                                so you always get the right answer even when you don't know the right words.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );

    function Card({ icon, title, children }: { icon: string; title: string; children: React.ReactNode }) {
        return (
            <div className="rounded-2xl border border-neutral-200 bg-white p-7">
                <div className="mb-5 flex h-9 w-9 items-center justify-center rounded-xl border border-amber-200 bg-amber-50">
                    <i className={`ti ${icon} text-lg text-amber-600`} aria-hidden />
                </div>
                <h2 className="mb-2 text-lg font-medium tracking-tight text-neutral-950">{title}</h2>
                <p className="text-[13px] leading-relaxed text-neutral-500">{children}</p>
            </div>
        );
    }
}