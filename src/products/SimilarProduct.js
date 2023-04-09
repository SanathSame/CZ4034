import React from "react";
import Image from '../related.jpg'

function SimilarProduct(props) {

    return (
        <div className="col">
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
                    <p className="card-text text-center text-muted mb-0">{Math.abs(props.price).toFixed(2) * 100}%</p>
                </div>
            </div>
        </div>
    );
}

export default SimilarProduct;
