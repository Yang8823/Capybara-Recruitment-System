import Hero from "../components/Hero";
import Navbar from "../components/Navbar"
import AboutImg from "../assets/1.jpg"

function Contact(){
    return(
        // empty fragment if we have multiple components inside return, we can create a <div> also
        <>
            <Navbar/>
            <Hero
                cName="hero-mid"
                heroImage="https://wallpapers.com/images/featured/capybara-n41z6e3moqckigqp.jpg"
                // heroImage={AboutImg}
                title="Contact"

                btnClass="hide"
            />             
        </>
    )
}

export default Contact;