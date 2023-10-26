import Hero from "../components/Hero";
import Navbar from "../components/Navbar"
import AboutImg from "../assets/1.jpg"

function About(){
    return(
        // empty fragment if we have multiple components inside return, we can create a <div> also
        <>
            <Navbar/>
            <Hero
                cName="hero-mid"
                // heroImage="HomeImg"
                heroImage={AboutImg}
                title="About"

                btnClass="hide"
            />            
        </>
    )
}

export default About;