import Image from "../../nillkin-case-1.jpg";
import { Link } from "react-router-dom";

function RelatedProduct(props) {
  return (
    <Link
      to="/products/1"
      className="col text-decoration-none"
      href="!#"
      replace
    >
      <div className="card shadow-sm">

        <img
          className="card-img-top bg-dark cover"
          height="200"
          alt=""
          src={Image}
        />
        <div className="card-body">
          <h5 className="card-title text-center text-dark text-truncate">
            {props.name}
          </h5>
          <p className="card-text text-center text-muted">{props.price}</p>
        </div>
      </div>
    </Link>
  );
}

export default RelatedProduct;
