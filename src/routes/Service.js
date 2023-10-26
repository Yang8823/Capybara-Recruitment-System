import Hero from "../components/Hero";
import Navbar from "../components/Navbar"
import AboutImg from "../assets/1.jpg"

function Service(){
    return(
        // empty fragment if we have multiple components inside return, we can create a <div> also
        <>
            <Navbar/>
            <Hero
                cName="hero-mid"
                heroImage="https://garden.spoonflower.com/c/3076350/p/f/m/Dlz7rE93O7n8SCIPDziNil2D29I4lWN5cJ-8jUPuTFGYSSO_gtw/Solid%20Caramel%20Brown.jpg"
                // heroImage={AboutImg}
                title="Service"

                btnClass="hide"
            />         
        </>
    )
}

export default Service;