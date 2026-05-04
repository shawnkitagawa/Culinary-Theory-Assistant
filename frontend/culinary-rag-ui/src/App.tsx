
import './App.css'
import { HomePage } from "./pages/HomePage"
import { Navigation } from './components/Navigation'
import { FeatureSection } from './components/FeatureSection'
import { FeatureSectionTeaser } from './components/FeatureSectionTeaser'
import { Footer } from "./components/Footer"

function App() {



  return (
    <div>
      <Navigation></Navigation>
      <HomePage></HomePage>
      <FeatureSection />
      <FeatureSectionTeaser />
      <Footer></Footer>

    </div>
  )

}

export default App
