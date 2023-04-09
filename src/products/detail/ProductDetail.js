import { Link } from "react-router-dom";
import ScrollToTopOnMount from "../../template/ScrollToTopOnMount";
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';
import React from "react";
import similar_products from "../../similarProducts.js";
import { useEffect, useState } from "react";
import SimilarProduct from "../SimilarProduct";
import product_reviews from "../../productReviews";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

function ProductDetail() {
  useEffect(() => {
    const name = sessionStorage.getItem('product_name');
    console.log("Name", name);
    findSimilarProducts(name);
  }, []);

  const [similarProducts, setSimilarProducts] = useState([]);
  const name = sessionStorage.getItem('product_name');
  const img = sessionStorage.getItem('image_link');
  const price = sessionStorage.getItem('price');
  const desc = sessionStorage.getItem('desc');
  const id = parseInt(sessionStorage.getItem('product_id'));
  const brand = sessionStorage.getItem('brand');


  const productReviews = product_reviews.filter(review => review.Product_ID === id && review.Review !== '');
  console.log("This is product product_reviews", productReviews);
  console.log("This is product id", name);

  function findSimilarProducts(productName) {
    const product = similar_products.find((p) => p.FIELD1 === productName);
    if (!product) {
      return []; // product not found
    }
    for (const [name, score] of Object.entries(product)) {
      if (name === "FIELD1" || parseFloat(score) >= 0) {
        continue; // ignore non-product fields and non-similar products
      }
      similarProducts.push({ name, score: parseFloat(score) });
    }
    similarProducts.sort((a, b) => a.score - b.score);
    console.log("Similar products", similarProducts); // sort by ascending similarity score
    setSimilarProducts(similarProducts.slice(1, 5)); // return top 4 similar products
  }


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
                <button className="btn btn-outline-dark py-2 w-100">Negative</button>
              </div>
            </div>

            <h4 className="mb-0">Details</h4>
            <hr />
            <dl className="row">

              <dt className="col-sm-4">Brand</dt>
              <dd className="col-sm-8 mb-3">{brand}</dd>

              <dt className="col-sm-4">Description</dt>
              <dd className="col-sm-8 mb-3">
                <span>{desc.slice(0, 500)}</span>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12 mb-4">
          <h4 className="mb-0">Reviews</h4>
          <hr />
          <div className="lead flex-shrink-0">
            <small>
              Reviews classified by the RoBERTa Model.
            </small>
            <Grid container spacing={10}>
              {productReviews.slice(0, 20).map((review, index) => (
                <React.Fragment key={index + 1}>
                  <Grid item xs={10}>
                    <Item>{review.Review}</Item>
                  </Grid>
                  <Grid item xs={2}>
                    <Item style={{ color: 'white', backgroundColor: review.RoBERTa ? 'green' : 'red' }}>{review.RoBERTa === 1 ? 'Positive' : 'Negative'}</Item>
                  </Grid>
                </React.Fragment>
              ))}
            </Grid>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12 mb-4">
          <hr />
          <h4 className="text-muted my-4">Related products</h4>
          <div className="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-3">
            {similarProducts.map((p, index) => (
              <SimilarProduct key={index + 1} name={p.name} price={p.score} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
