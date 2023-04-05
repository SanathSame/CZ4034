import { Link } from "react-router-dom";
import ScrollToTopOnMount from "../../template/ScrollToTopOnMount";
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';


const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));
function ProductDetail() {


  const name = sessionStorage.getItem('product_name');
  const img = sessionStorage.getItem('image_link');
  const price = sessionStorage.getItem('price');
  const desc = sessionStorage.getItem('desc');


  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded mb-4">
        <ol className="breadcrumb p-3">
          <li className="breadcrumb-item">
            <Link className="text-decoration-none link-secondary" to="/products">
              All Products
            </Link>
          </li>
          <li className="breadcrumb-item">
            <a className="text-decoration-none link-secondary" href="!#">

            </a>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            {name}
          </li>
        </ol>
      </nav>
      <div className="row mb-4">
        <div className="d-none d-lg-block col-lg-1">
          <div className="image-vertical-scroller">
          </div>
        </div>
        <div className="col-lg-6">
          <div className="row">
            <div className="col-12 mb-4">
              <img
                className="border rounded ratio ratio-1x1"
                alt=""
                src={img}
              />
            </div>
          </div>
        </div>

        <div className="col-lg-5">
          <div className="d-flex flex-column h-100">
            <h2 className="mb-1">{name}</h2>
            <h4 className="text-muted mb-4">{price}</h4>

            <div className="row g-3 mb-4">
              <div className="col">
                <button className="btn btn-outline-dark py-2 w-100">
                  Positive
                </button>
              </div>
              <div className="col">
                <button className="btn btn-dark py-2 w-100">Negative</button>
              </div>
            </div>

            <h4 className="mb-0">Details</h4>
            <hr />
            <dl className="row">

              <dt className="col-sm-4">Category</dt>
              <dd className="col-sm-8 mb-3"> Complexion Balm</dd>

              <dt className="col-sm-4">Brand</dt>
              <dd className="col-sm-8 mb-3">Hermes</dd>

              <dt className="col-sm-4">Description</dt>
              <dd className="col-sm-8 mb-3">
                <p>{desc}</p>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12 mb-4">
          <h4 className="mb-0">Description</h4>
          <hr />
          <p className="lead flex-shrink-0">
            <small>
              Reviews classified by the RoBERTa Model.
            </small>
            <Grid container spacing={2}>
              <Grid item xs={10}>
                <Item>xs=10</Item>
              </Grid>
              <Grid item xs={2}>
                <Item>xs=2</Item>
              </Grid>
            </Grid>
          </p>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
