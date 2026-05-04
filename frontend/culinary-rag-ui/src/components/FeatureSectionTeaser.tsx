

export function FeatureSectionTeaser() {




    return (
        <section className="min-h-screen bg-neutral-50 px-6 py-24">
            <div className="mx-auto max-w-5xl text-center">
                <h1 className="text-5xl font-bold leading-[1.05] tracking-tight text-black md:text-7xl">
                    Culinary AI 2.0
                    <br />
                    is Coming ......
                </h1>

                <h2 className="mt-8 text-lg font-semibold tracking-tight text-neutral-700 md:text-2xl">
                    Smarter answers, clearer sources, easier culinary research.
                </h2>
            </div>

            <div className="mx-auto mt-16 max-w-6xl space-y-4">
                {/* First row */}
                <div className="grid grid-cols-[2fr_1fr] gap-4">
                    <div className="rounded-lg border border-neutral-300 bg-white p-8">
                        <div className="mb-6 text-2xl text-red-500">♡</div>

                        <h2 className="text-2xl font-medium tracking-tight text-black">
                            Better Questions
                        </h2>

                        <p className="mt-5 max-w-2xl text-base leading-7 text-neutral-700">
                            Culinary AI 2.0 will improve how the system understands user intent,
                            expands vague questions, and finds more relevant culinary knowledge
                            before generating an answer.
                        </p>
                    </div>

                    <div className="rounded-lg border border-neutral-300 bg-white p-8">
                        <div className="mb-6 text-2xl text-red-500">♙</div>

                        <h2 className="text-2xl font-medium tracking-tight text-black">
                            More Reliable Answers
                        </h2>

                        <p className="mt-5 text-base leading-7 text-neutral-700">
                            Responses will be improved to stay closer to trusted culinary
                            knowledge.
                        </p>
                    </div>
                </div>

                {/* Second row */}
                <div className="grid grid-cols-[1fr_2fr] gap-4">
                    <div className="rounded-lg border border-neutral-300 bg-white p-8">
                        <div className="mb-6 text-2xl text-red-500">◎</div>

                        <h2 className="text-2xl font-medium tracking-tight text-black">
                            Clearer Sources
                        </h2>

                        <p className="mt-5 text-base leading-7 text-neutral-700">
                            Users will see where the answer came from more easily.
                        </p>
                    </div>

                    <div className="rounded-lg border border-neutral-300 bg-white p-8">
                        <div className="mb-6 text-2xl text-red-500">✧</div>

                        <h2 className="text-2xl font-medium tracking-tight text-black">
                            Search That Understands Meaning
                        </h2>

                        <p className="mt-5 max-w-2xl text-base leading-7 text-neutral-700">
                            The app finds relevant culinary knowledge based on meaning, not just
                            exact keywords.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}