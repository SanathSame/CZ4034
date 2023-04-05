import React from "react";
import { Link } from "react-router-dom";
import Product from "./Product";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ScrollToTopOnMount from "../template/ScrollToTopOnMount";
import Slider from "@mui/material/Slider";
import { useEffect } from "react";

const categories = [
  "Sun Protection",
  "Toner",
  "Oil Cleanser",
  "Moisturizer",
  "Makeup",
  "Serum/Ampoule"
];

const skin_type = ["Combination", "Dry", "Normal", "Oily"];

const skin_concern = ["Acne", "Anti-aging/Wrinkles", "Dryness/Hydration", "Oil Control/Pores", "Pigmentation", "Redness", "Sensitive"];

function FilterMenuLeft() {
  const [range, setRange] = React.useState([1, 95]);


  function handleChanges(event, newValue) {
    setRange(newValue);
  }
  return (
    <ul className="list-group list-group-flush rounded">
      <li className="list-group-item d-none d-lg-block">
        <h5 className="mt-1 mb-2">Browse</h5>
        <div className="d-flex flex-wrap my-2">
          {categories.map((v, i) => {
            return (
              <Link
                key={i}
                to="/products"
                className="btn btn-sm btn-outline-dark rounded-pill me-2 mb-2"
                replace
              >
                {v}
              </Link>
            );
          })}
        </div>
      </li>
      <li className="list-group-item">
        <h5 className="mt-1 mb-1">Skin Type</h5>
        <div className="d-flex flex-column">
          {skin_type.map((v, i) => {
            return (
              <div key={i} className="form-check">
                <input className="form-check-input" type="checkbox" />
                <label className="form-check-label" htmlFor="flexCheckDefault">
                  {v}
                </label>
              </div>
            );
          })}
        </div>
      </li>
      <li className="list-group-item">
        <h5 className="mt-1 mb-1">Skin Concern</h5>
        <div className="d-flex flex-column">
          {skin_concern.map((v, i) => {
            return (
              <div key={i} className="form-check">
                <input className="form-check-input" type="checkbox" />
                <label className="form-check-label" htmlFor="flexCheckDefault">
                  {v}
                </label>
              </div>
            );
          })}
        </div>
      </li>
      <li className="list-group-item">
        <h5 className="mt-1 mb-2">Price Range</h5>
        <div className="d-grid d-block mb-3">
          <Slider value={range} onChange={handleChanges} valueLabelDisplay="auto" />
        </div>
      </li>
      <button className="btn btn-dark">Apply</button>
    </ul>
  );
}


function ProductList() {
  const [searchTerm, setsearchTerm] = useState('');
  const [products, setproducts] = useState([]);

  useEffect(() => {
    handleSearch()
  }, [])
  const handleChange = event => {
    setsearchTerm(event.target.value);

    console.log('value is:', event.target.value);
  };
  async function handleSearch() {
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };

    await fetch("http://localhost:8983/solr/info/select?indent=true&q.op=OR&q=*%3A*&useParams=", requestOptions)
      .then(response => response.json())
      .then(data => setproducts(data.response.docs))
      .catch(error => console.log('error', error));
  }
  console.log("Products value", products);


  return (
    <div className="container mt-5 py-4 px-xl-5">
      <ScrollToTopOnMount />
      <nav aria-label="breadcrumb" className="bg-custom-light rounded">
        <ol className="breadcrumb p-3 mb-0">
          <li className="breadcrumb-item">
            <Link
              className="text-decoration-none link-secondary"
              to="/products"
              replace>
              All Products
            </Link>
          </li>
        </ol>
      </nav>

      <div className="h-scroller d-block d-lg-none">
        <nav className="nav h-underline">
          {categories.map((v, i) => {
            return (
              <div key={i} className="h-link me-2">
                <Link
                  to="/products"
                  className="btn btn-sm btn-outline-dark rounded-pill"
                  replace
                >
                  {v}
                </Link>
              </div>
            );
          })}
        </nav>
      </div>

      <div className="row mb-3 d-block d-lg-none">
        <div className="col-12">
          <div id="accordionFilter" className="accordion shadow-sm">
            <div className="accordion-item">
              <h2 className="accordion-header" id="headingOne">
                <button
                  className="accordion-button fw-bold collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#collapseFilter"
                  aria-expanded="false"
                  aria-controls="collapseFilter"
                >
                  Filter Products
                </button>
              </h2>
            </div>
            <div
              id="collapseFilter"
              className="accordion-collapse collapse"
              data-bs-parent="#accordionFilter"
            >
              <div className="accordion-body p-0">
                <FilterMenuLeft />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row mb-4 mt-lg-3">
        <div className="d-none d-lg-block col-lg-3">
          <div className="border rounded shadow-sm">
            <FilterMenuLeft />
          </div>
        </div>
        <div className="col-lg-9">
          <div className="d-flex flex-column h-100">
            <div className="row mb-3">
              <div className="col-lg-3 d-none d-lg-block">
                <select
                  className="form-select"
                  aria-label="Default select example"
                  defaultValue=""
                >
                  <option value="">All Brands</option>
                  <option value="1">NEOGEN</option>
                  <option value="2">COSRX</option>
                  <option value="3">BENTON</option>
                  <option value="4">BENTON</option>
                  <option value="5">BENTON</option>
                  <option value="6">BENTON</option>
                  <option value="7">BENTON</option>
                  <option value="8">BENTON</option>
                  <option value="9">BENTON</option>
                  <option value="10">BENTON</option>

                </select>
              </div>
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <div className="input-group">
                  <input
                    className="form-control"
                    type="text"
                    placeholder="Search products..."
                    aria-label="search input"
                    value={searchTerm}
                    onChange={handleChange}
                  />
                  <button className="btn btn-outline-dark" onClick={handleSearch}>
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                </div>
                {/* <button
                  className="btn btn-outline-dark ms-2 d-none d-lg-inline"
                  onClick={changeViewType}
                >
                  <FontAwesomeIcon
                    icon={["fas", viewType.grid ? "th-list" : "th-large"]}
                  />
                </button> */}
              </div>
            </div>
            <div
              className={
                "row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 " +
                "row-cols-xl-3"
              }
            >
              {products.map(product => (
                <Product key={product.product_ID} Img_link={product.Img_link} name={product.product_name} price={product.price} brand={product.product_brand} desc={product.product_description} />
              ))}
            </div>
            <div className="d-flex align-items-center mt-auto">
              <span className="text-muted small d-none d-md-inline">
                Out of 553 possible products
              </span>
              {/* <nav aria-label="Page navigation example" className="ms-auto">
                <ul className="pagination my-0">
                  <li className="page-item">
                    <a className="page-link" href="!#">
                      Previous
                    </a>
                  </li>
                  <li className="page-item active">
                    <a className="page-link" href="/products">
                      1
                    </a>
                  </li>
                  <li className="page-item">
                    <a className="page-link" href="!#">
                      2
                    </a>
                  </li>
                  <li className="page-item">
                    <a className="page-link" href="!#">
                      3
                    </a>
                  </li>
                  <li className="page-item">
                    <a className="page-link" href="!#">
                      Next
                    </a>
                  </li>
                </ul>
              </nav> */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductList;
