import { Link } from "react-router-dom";
import "../css/NavBar.css"

function NavBar() {
    return <nav className="navbar">
        <div className="navbar-brand">
            <Link to="/">Taqwa</Link>
        </div>
        <div className="navbar-links">
            <Link to="/" className="nav-link">Предложить вопрос</Link>
            <Link to="/review" className="nav-link">Проверить вопросы</Link>
        </div>
    </nav>
}

export default NavBar