
import './App.css'
import { HomePage } from "./pages/HomePage"
import { Navigation } from './components/Navigation'
import { Routes, Route } from "react-router-dom"
import { Footer } from './components/Footer'
import Demo from './pages/Demo'

function App() {

  const isDemoPage = location.pathname === "/demo";

  return (
    <div>
      <Navigation variant={isDemoPage ? "solid" : "glass"} />
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/demo" element={<Demo />}></Route>
      </Routes>

      {!isDemoPage && <Footer />}



    </div>
  )

}

export default App
