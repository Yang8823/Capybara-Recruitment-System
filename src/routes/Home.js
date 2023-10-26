import Hero from "../components/Hero";
import Navbar from "../components/Navbar"
import HomeImg from "../assets/1.jpg"
import Destination from "../components/Destination";

function Home(){
    return(
        // empty fragment if we have multiple components inside return, we can create a <div> also
        <>
            <Navbar/>
            <Hero
                cName="hero"
                // heroImage="HomeImg"
                heroImage="https://wallpapers.com/images/hd/showering-golden-capybara-n5e4qtbgnj7hcmmb.jpg"
                title="AI-powered CV scanning and rating"
                text="Optimize your recruitment process"
                buttonText="Get Started"
                url="/"
                btnClass="show"
            />
            <Destination/>
        </>
    )
}

export default Home;