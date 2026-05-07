import culinary_logo from "../../public/culinary_logo.svg"

type NavigationProps = {
    variant?: "glass" | "solid";
}


export function Navigation({ variant = "glass" }: NavigationProps) {
    const navClass =
        variant === "glass"
            ? "text-white/80 fixed top-0 z-20 w-full border-b border-white/20 bg-black/20 backdrop-blur-md"
            : "text-neutral-900 fixed top-0 z-20 w-full border-b border-neutral-200 bg-white";


    return (

        <nav className={navClass}>
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                    <img src={culinary_logo} className="h-15 w-15 object-contain rounded-4xl " alt="Culinary AI Logo" />
                    <span className="self-center text-2xl text-heading font-semibold whitespace-nowrap">Culinary Rag AI</span>
                </a>
                <button data-collapse-toggle="navbar-default" type="button" className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-body rounded-base md:hidden hover:bg-neutral-secondary-soft hover:text-heading focus:outline-none focus:ring-2 focus:ring-neutral-tertiary" aria-controls="navbar-default" aria-expanded="false">
                    <span className="sr-only">Open main menu</span>
                    <svg className="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M5 7h14M5 12h14M5 17h14" /></svg>
                </button>
                <div className="hidden w-full md:block md:w-auto" id="navbar-default">
                    <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-default rounded-base bg-neutral-secondary-soft md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-neutral-primary">
                        <li className={variant === "glass" ? "hover:text-white" : "hover:text-black"}>
                            <a href="/" className="block py-2 px-3 bg-brand rounded md:bg-transparent md:text-fg-brand md:p-0" aria-current="page">Home</a>
                        </li>
                        <li className={variant === "glass" ? "hover:text-white" : "hover:text-black"}>
                            <a href="/demo" className="block py-2 px-3 text-heading rounded hover:bg-neutral-tertiary md:hover:bg-transparent md:border-0 md:hover:text-fg-brand md:p-0 md:dark:hover:bg-transparent">Demo</a>
                        </li>
                        <li className={variant === "glass" ? "hover:text-white" : "hover:text-black"}>
                            <a href="#" className="block py-2 px-3 text-heading rounded hover:bg-neutral-tertiary md:hover:bg-transparent md:border-0 md:hover:text-fg-brand md:p-0 md:dark:hover:bg-transparent">Mobile Coming Soon...</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

    )
}