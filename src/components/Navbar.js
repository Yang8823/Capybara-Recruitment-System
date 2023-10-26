import { Component } from "react";
import "./NavbarStyles.css";
import { MenuItems } from "./MenuItems";
import { Link } from "react-router-dom";

class Navbar extends Component{
    state = {clicked: false};
    // a function to handle click
    handleClick = () =>{
        this.setState({clicked: !this.state.clicked})
    }

    // use render because we are extending out components
    render(){
        return(
            <nav className="NavbarItems">
                <h1 className="navbar-logo">Capybara Recruitment System</h1>
                
                <div className="menu-icons" onClick={this.handleClick}>
                    {/* make it as state for it to change and ifelse */}
                    <i className={this.state.clicked ? "fas fa-times" : "fas fa-bars"}></i>
                </div>
                
                
                <ul className={this.state.clicked ? "nav-menu active" : "nav-menu"}>
                    {/* Make array to print menu item */}
                    {MenuItems.map((item, index) =>{
                        return(
                            /*make list tag dynamic*/
                            <li key={index}>
                                <Link className={item.cName} to={item.url}>
                                    {/*make icon tag dynamic*/}
                                    <i class={item.icon}></i>{item.title}
                                </Link>
                            </li>
                        )
                    })}
                    <button>Sign Up</button>
                </ul>
            </nav>
        )
    }
}

// if we are importing component we need to make sure that 
// component is allowing other file to import that component by:
export default Navbar;