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




function ProductList() {
  const [searchTerm, setsearchTerm] = useState('');
  const [products, setproducts] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState('');

  useEffect(() => {
    retrieveProducts()
  }, [])
  const handleChange = event => {
    setsearchTerm(event.target.value);

    console.log('value is:', event.target.value);
  };
  async function retrieveProducts() {
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };

    await fetch("http://localhost:8983/solr/ir/select?indent=true&q.op=OR&q=*%3A*&useParams=", requestOptions)
      .then(response => response.json())
      .then(data => setproducts(data.response.docs))
      .catch(error => console.log('error', error));
  }
  console.log("Products value", products);

  async function handleExactSearch() {
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    const term = sessionStorage.getItem('Search');
    console.log('Search term is',);

    await fetch("http://localhost:8983/solr/ir/select?indent=true&q.op=OR&q=product_description%3A*" + term + "*%20OR%20product_name%3A*" + term + "*&useParams=", requestOptions)
      .then(response => response.json())
      .then(data => setproducts(data.response.docs))
      .catch(error => console.log('error', error));
  }
  const handleSelectBrand = (event) => {
    setSelectedBrand(event.target.value);
    console.log('selected brand', selectedBrand);
  };


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
                  onChange={handleSelectBrand}
                >
                  <option value="">All Brands</option>
                  <option value="NEOGEN">NEOGEN</option>
                  <option value="COSRX">COSRX</option>
                  <option value="BENTON">BENTON</option>
                  <option value="HANSKIN">HANSKIN</option>
                  <option value="KLAIRS">KLAIRS</option>
                  <option value="NATURIUM">NATURIUM</option>
                  <option value="EXCLUSIVE">EXCLUSIVE</option>
                </select>
              </div>
              <div className="col-lg-9 col-xl-5 offset-xl-4 d-flex flex-row">
                <div className="input-group">
                  <input
                    className="form-control"
                    type="text"
                    placeholder="Search products..."
                    aria-label="search input"
                    value={sessionStorage.setItem('Search', searchTerm)}
                    onChange={handleChange}
                  />
                  <button className="btn btn-outline-dark" onClick={handleExactSearch}>
                    <span>EM</span>
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                  <button className="btn btn-outline-dark" onClick={retrieveProducts}>
                    <span>DVS</span>
                    <FontAwesomeIcon icon={["fas", "search"]} />
                  </button>
                </div>
              </div>
            </div>
            <div
              className={
                "row row-cols-1 row-cols-md-2 row-cols-lg-2 g-3 mb-4 flex-shrink-0 " +
                "row-cols-xl-3"
              }
            >
              {products.map(product => (
                <Product key={product.product_ID} id={product.product_ID} Img_link={product.Img_link} name={product.product_name} price={product.price} brand={product.product_brand} desc={product.product_description} />
              ))}
            </div>
            <div className="d-flex align-items-center mt-auto">
              <span className="text-muted small d-none d-md-inline">
                Out of 553 possible products
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  function FilterMenuLeft() {
    const [range, setRange] = React.useState([1, 95]);
    const [selectedValues, setSelectedValues] = React.useState([]);
    const [skinValues, setSkinValues] = React.useState([]);
    const [typeSelected, setTypeSelected] = useState('');

    function handleChanges(event, newValue) {
      setRange(newValue);
    }

    async function handleFilterApply() {
      var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };

      await fetch("http://localhost:8983/solr/ir/select?indent=true&q.op=AND&useParams=&q=product_brand%3ANATURIUM%0Aprice_num%3A%5B20%20TO%2030%5D%0Askin_type%3ACombination%0Aproduct_type%3AMoisturizer%0Askin_concern%3AAnti-Aging%2FWrinkles", requestOptions)
        .then(response => response.json())
        .then(data => setproducts(data.response.docs))
        .catch(error => console.log('error', error));
    }

    const handleCheckBoxChange = (event) => {
      const value = event.target.value;
      console.log("Checkbox value", value);
      if (event.target.checked) {
        // Add the selected value to the array of selected values
        setSelectedValues([...selectedValues, value]);
      } else {
        // Remove the unselected value from the array of selected values
        setSelectedValues(selectedValues.filter((val) => val !== value));
      }
    };

    const handleSkinConcernChange = (event) => {
      const value = event.target.value;
      console.log("Checkbox value", value);
      if (event.target.checked) {
        // Add the selected value to the array of selected values
        setSkinValues([...skinValues, value]);
      } else {
        // Remove the unselected value from the array of selected values
        setSkinValues(skinValues.filter((val) => val !== value));
      }
    };

    const handleProductClick = (event) => {
      setTypeSelected(event.target.value);
      console.log('Product type is', typeSelected);
    };
    return (
      <ul className="list-group list-group-flush rounded">
        <li className="list-group-item d-none d-lg-block">
          <h5 className="mt-1 mb-2">Browse</h5>
          <div className="d-flex flex-wrap my-2">
            {categories.map((v, i) => {
              return (
                <button
                  key={i}
                  className="btn btn-sm btn-outline-dark rounded-pill me-2 mb-2"
                  value={v}
                  onClick={handleProductClick}
                >
                  {v}
                </button>
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
                  <input className="form-check-input" type="checkbox" onChange={handleCheckBoxChange} value={v} />
                  <label className="form-check-label" htmlFor="flexCheckDefault">
                    {v}
                  </label>
                </div>
              );
            })}
            <p>Selected values: {selectedValues.join(', ')}</p>
          </div>
        </li>
        <li className="list-group-item">
          <h5 className="mt-1 mb-1">Skin Concern</h5>
          <div className="d-flex flex-column">
            {skin_concern.map((v, i) => {
              return (
                <div key={i} className="form-check">
                  <input className="form-check-input" type="checkbox" value={v} onChange={handleSkinConcernChange} />
                  <label className="form-check-label" htmlFor="flexCheckDefault">
                    {v}
                  </label>
                </div>
              );
            })}
            <p>Selected values: {skinValues.join(', ')}</p>
          </div>
        </li>
        <li className="list-group-item">
          <h5 className="mt-1 mb-2">Price Range</h5>
          <div className="d-grid d-block mb-3">
            <Slider value={range} onChange={handleChanges} valueLabelDisplay="auto" />
          </div>
        </li>
        <button className="btn btn-dark" onClick={handleFilterApply}>Apply</button>
      </ul>
    );
  }
}

export default ProductList;
