import { useHistory } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function Product(props) {
  const history = useHistory();


  function handleClick() {
    sessionStorage.setItem('product_id', props.id);
    sessionStorage.setItem('price', props.price);
    sessionStorage.setItem('product_name', props.name);
    sessionStorage.setItem('image_link', props.Img_link);
    sessionStorage.setItem('brand', props.brand);
    sessionStorage.setItem('desc', props.desc);


    history.push('/products/review');
  }

  return (
    <div className="col">
      <div className="card shadow-sm">
        <img
          className="card-img-top bg-dark cover"
          height="200"
          alt=""
          src={props.Img_link}
        />
        <div className="card-body">
          <h5 className="card-title text-center text-dark text-truncate">
            {props.name}
          </h5>
          <p className="card-text text-center text-muted mb-0">{props.price}</p>
          <div className="d-grid d-block">
            <button className="btn btn-outline-dark mt-3" onClick={handleClick}>
              <FontAwesomeIcon icon="fa-sharp fa-solid fa-star-sharp-half-stroke" /> View reviews
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Product;
