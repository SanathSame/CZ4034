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
    if (term.length > 1)
      console.log('Search term is',);
    let query = '';
    // split the search term into individual words
    const words = term.split(' ');
    // construct the query for each word
    words.forEach((word, index) => {
      query += `product_name:*${word} OR product_description:*${word}*`;
      if (index !== words.length - 1) {
        query += ' AND ';
      }
    });

    // construct the final URL
    const url = `http://localhost:8983/solr/ir/select?indent=true&q.op=OR&q=${encodeURIComponent(query)}&useParams=`;

    await fetch(url, requestOptions)
      .then(response => response.json())
      .then(data => setproducts(data.response.docs))
      .catch(error => console.log('error', error));
  }

  async function handleDenseSearch() {

    const qv = '[-0.64,0.22,0.31,0.69,-0.21,-0.58,0.60,-0.13,0.31,-0.11,-0.37,-0.45,-0.33,\n 0.67,0.60,0.67,-0.18,0.52,0.08,-0.30,0.42,0.47,0.93,0.11,-0.05,-0.07,\n -0.05,-1.07,-0.51,-0.03,-0.48,0.53,0.07,-0.07,0.41,-0.47,-0.67,-0.21,0.41,\n 0.21,0.03,-0.65,0.83,0.07,-0.25,-0.58,-3.69,0.28,0.01,-0.50,-0.21,-0.29,\n 0.54,0.20,0.18,0.82,0.03,-0.56,1.60,0.22,0.11,0.54,-0.72,0.02,-0.07,0.66,\n 0.21,-0.10,-0.67,0.28,0.08,0.46,0.54,0.12,-0.08,-0.36,-0.38,1.25,-0.58,\n -0.26,0.24,-0.32,0.02,-0.85,0.55,0.26,0.58,-0.52,-0.63,0.20,0.19,0.08,\n 0.43,0.35,0.11,-0.21,0.13,0.13,-0.24,-0.01,-0.61,1.07,0.40,-0.35,-0.11,\n 0.05,-1.37,0.06,-0.13,0.23,0.19,0.51,-0.71,0.04,0.51,0.25,0.37,-0.38,0.68,\n -0.43,0.49,-0.03,0.18,0.07,-0.04,0.04,0.05,-1.54,0.37,0.90,0.03,0.34,\n -0.40,0.11,-0.48,-0.64,-0.00,0.16,-0.10,0.08,-1.20,-0.61,-0.48,-0.75,0.26,\n -0.02,0.22,0.58,-0.54,-0.33,-0.14,0.02,-1.13,-0.83,-0.33,-0.78,0.90,-0.05,\n -0.20,0.89,0.26,0.65,0.16,0.51,-0.19,0.04,0.71,0.43,-0.10,-0.24,0.01,0.01,\n 0.71,-0.74,-0.01,0.51,0.53,0.27,0.81,-0.11,-0.73,0.08,-0.49,-0.09,0.12,\n 0.40,0.34,0.87,-0.06,0.81,-1.59,-0.34,0.66,0.42,0.42,0.18,-0.53,0.61,\n -0.08,-0.21,-0.14,0.58,-0.18,0.47,0.10,2.11,0.06,-0.10,-0.16,-0.15,-0.60,\n -0.55,-0.65,0.43,-0.30,-0.63,-0.48,-0.30,0.10,0.31,-0.39,-0.66,-0.48,0.52,\n -0.02,-0.45,-0.71,-0.47,0.10,-1.57,0.08,-0.96,-0.39,-0.27,-0.38,0.26,0.14,\n -0.38,0.27,0.39,-0.36,0.85,0.19,-0.23,-0.25,0.00,-0.15,-0.58,0.00,-0.05,\n -0.03,0.10,-0.09,0.39,0.14,0.07,-0.23,0.18,-0.82,-0.70,-0.16,0.01,-0.54,\n 0.39,-0.14,0.02,-0.05,-0.08,-0.05,-0.23,-0.04,-0.81,-0.41,0.61,0.20,-0.40,\n 0.94,-0.37,-0.01,-0.11,0.21,0.16,-0.70,0.08,-0.46,-0.56,0.39,-0.44,0.76,\n 0.26,-0.50,0.69,-0.17,0.32,0.15,-0.76,0.13,-0.40,0.33,0.68,-0.43,0.69,\n -0.87,0.94,0.39,-0.13,-0.18,0.54,-4.43,0.44,-0.47,-0.01,-0.06,0.49,0.94,\n 0.49,-0.43,0.13,0.03,0.60,-0.10,0.04,-0.60,-0.42,1.07,0.06,0.10,0.50,\n -0.73,0.13,0.50,-0.40,0.50,0.33,-0.20,0.05,-0.12,0.53,-0.18,-0.92,0.32,\n -0.58,-0.11,-0.05,-0.11,-0.58,0.73,-0.44,0.57,-0.84,-0.04,-0.04,0.71,\n -0.32,0.03,1.14,0.36,0.67,0.10,0.26,0.24,0.00,-0.15,-0.42,0.16,-0.26,\n -0.53,0.27,0.88,0.33,-0.69,0.23,0.35,-1.10,0.06,-0.19,-1.33,0.52,-0.96,\n -0.11,0.07,-1.15,0.53,-0.49,0.05,0.03,-0.23,0.12,-0.59,-0.30,0.07,0.79,\n -0.43,0.84,-0.43,0.71,-0.32,0.42,-0.22,-0.03,0.55,-0.06,-0.06,0.95,0.52,\n 0.14,0.54,0.03,1.02,-0.17,-0.28,0.16,-0.01,0.02,-0.47,-0.19,0.44,-0.16,\n 0.08,0.26,-0.26,-0.08,0.16,-0.40,-0.39,0.08,0.65,0.04,-0.22,-0.34,-0.75,\n -0.19,-0.66,0.19,0.20,0.75,-0.07,-0.31,-0.11,-0.70,-1.37,-0.14,0.28,0.15,\n 0.27,-0.99,0.37,-0.18,0.99,-0.06,-0.48,0.20,-0.33,0.33,0.41,-0.50,-0.19,\n 0.08,0.02,0.19,0.14,-0.91,0.47,0.34,-0.41,-0.45,-0.45,-0.44,0.65,-0.25,\n -1.28,-0.61,0.10,0.72,0.69,-0.19,-0.10,0.44,-0.51,0.11,-0.32,0.01,-0.00,\n 0.09,0.34,-0.20,0.51,0.17,-0.20,-0.10,-0.05,0.13,0.39,0.79,-0.17,0.07,\n -0.32,0.70,-0.21,0.13,-0.09,-1.03,-0.30,-0.75,0.56,1.09,0.22,0.43,-0.29,\n 0.38,-0.01,0.15,0.97,0.30,-0.26,0.24,-0.12,0.09,0.07,0.02,-0.06,0.22,0.27,\n -0.32,-0.15,-0.51,-0.46,0.19,-0.45,0.40,0.74,-0.46,-0.06,-0.31,-0.50,\n -0.05,0.66,-0.07,-0.65,-0.06,0.22,0.14,-1.25,-0.19,-0.41,-0.44,0.25,0.97,\n 0.09,0.02,1.09,-0.79,0.40,0.44,-0.08,0.26,0.15,0.19,0.39,0.23,-0.24,-0.57,\n 0.94,-0.27,0.11,-0.53,-0.84,-0.27,-0.34,0.53,-0.18,0.23,0.46,0.11,0.22,\n 1.31,0.18,-0.55,-0.80,0.25,0.11,0.01,-0.38,0.33,0.50,0.00,0.52,-0.86,\n -0.25,0.21,-0.04,-0.00,0.65,-0.10,-0.21,-0.65,0.14,0.46,-0.88,0.55,-0.59,\n -0.42,0.10,0.73,0.27,-0.03,-0.63,0.10,-0.07,0.79,0.99,-0.60,-0.22,0.22,\n -0.16,0.05,-0.34,-0.12,0.48,0.43,0.29,0.32,-0.04,-0.31,-0.66,-0.41,-0.22,\n 0.93,0.07,0.31,0.73,-0.68,-0.02,0.79,0.38,-0.33,0.24,0.67,-0.24,-1.18,\n -0.22,-0.02,-0.60,0.08,-0.28,-1.15,-0.74,0.34,-0.61,-0.10,0.77,-0.25,\n -0.89,-0.23,0.35,0.05,0.05,-0.37,-0.16,0.39,0.98,0.38,0.02,0.30,0.22,\n -0.80,-0.75,-0.19,-0.17,0.06,0.20,-0.14,-0.23,-0.27,0.41,0.68,0.36,-0.80,\n 0.68,-0.14,-0.17,0.05,0.38,0.50,0.15,-0.14,0.04,-0.20,-0.19,-0.40,-0.23,\n -0.14,0.27,0.75,-0.18,-0.13,0.04,-0.38,0.44,0.07,-0.12,0.23,0.01,0.51,\n -0.03,0.12,0.57,-0.08,0.53,0.27,0.91,0.45,-0.50,0.24,-0.16,0.82,-0.62,\n -0.16,-0.12,-0.05,0.68,0.50,-0.24,-0.78,0.12,0.13,0.11,-1.10,-0.73,-0.36,\n 0.38,0.44,0.04,-0.38,0.07,0.13,-0.74,0.33,-0.53,-0.10,0.22,0.40,-0.29,\n -0.73,0.69,0.42,0.36,-0.28,0.51,0.39,0.92,0.19,-0.29,-0.31,-0.15,-0.08,\n -0.06,-0.30,-0.19,-0.02,-0.20,-0.55,0.49,-0.83,-0.08,-0.52,0.47,-0.48]';

    const url = "http://localhost:8983/solr/ir/select?indent=true&q.op=OR&&q={!knn f=feature_vector topK=5}" + qv;
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };

    fetch(url, requestOptions)
      .then(response => response.json())
      .then(data => setproducts(data.response.docs))
      .catch(error => console.log('error', error));
  };

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
                  <button className="btn btn-outline-dark" onClick={handleDenseSearch}>
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
      let query = '';

      // add the selected brand filter to the query
      if (selectedBrand !== '')
        query += `product_brand:${selectedBrand}`;

      // add the selected skin type filters to the query
      if (selectedValues.length > 0) {
        query += '\n';
        selectedValues.forEach((value, index) => {
          query += `skin_type:${value}`;
          if (index !== selectedValues.length - 1) {
            query += ' OR ';
          }
        });
      }
      // add the selected skin concern filters to the query
      if (skinValues.length > 0) {
        query += '\n';
        skinValues.forEach((value, index) => {
          query += `skin_concern:${value}`;
          if (index !== skinValues.length - 1) {
            query += ' OR ';
          }
        });
      }
      // add the selected price range filter to the query
      query += `\nprice_num:[${range[0]} TO ${range[1]}]`;
      // add the selected product type filter to the query
      if (typeSelected.length > 0) {
        const typeWords = typeSelected.split(' ');
        query += '\n';
        typeWords.forEach((word, index) => {
          query += `product_type:${word}`;
          if (index !== typeWords.length - 1) {
            query += ' OR ';
          }
        });
      }
      console.log('Query is', query);

      // construct the final URL
      const url = `http://localhost:8983/solr/ir/select?indent=true&q.op=AND&q=${encodeURIComponent(query)}&useParams=`;
      var requestOptions = {
        method: 'GET',
        redirect: 'follow'
      };

      await fetch(url, requestOptions)
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
