import "./HeroStyles.css"

function Hero(props){
    return(
        // empty fragment if we have multiple components inside return, we can create a <div> also
        <>
            <div className={props.cName}>
                <img alt="HerpImg" src={props.heroImage}/>
            </div>

            <div className="hero-text">
                <h1>{props.title}</h1>
                <p>{props.text}</p>
                <a href={props.url} className={props.btnClass}>
                    {props.buttonText}
                </a>
            </div>

        </>
    )
}

export default Hero;