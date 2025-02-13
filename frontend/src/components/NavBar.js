import { Link } from "react-router-dom";
import "../css/NavBar.css"

function NavBar() {
    return <nav className="navbar">
        <div className="navbar-brand">
            <Link to="/">Taqwa</Link>
        </div>
        <div className="navbar-links">
            <Link to="/" className="nav-link">Проверить вопросы</Link>
            <Link to="/suggest" className="nav-link">Предложить вопрос</Link>
        </div>
    </nav>
}

export default NavBar