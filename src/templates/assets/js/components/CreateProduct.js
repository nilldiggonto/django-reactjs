import React, {useState,useEffect} from 'react';
import TagsInput from 'react-tagsinput';
import 'react-tagsinput/react-tagsinput.css';
import Dropzone from 'react-dropzone'


const CreateProduct = (props) => {

    const [productVariantPrices, setProductVariantPrices] = useState([])

    const [productVariants, setProductVariant] = useState([
        {
            option: 1,
            tags: []
        }
    ])

    const [file,setFile] = useState([])
    const [updatePage,setUpdatePage] = useState(0)
    const [image, setImage] = useState(null);
    // const [imgSrc, setImgSrc] = useState([])

    useEffect(() => {
        // Get the current URL
        const url = window.location.href;

        // Check if the URL contains "update"
        if (url.includes("update")) {
            // Extract the ID from the URL
            const id = url.match(/\/update\/(\d+)/)[1];
            
            fetch('/product/api/details/' + id +'/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ProductName').value = data.title;
                    document.getElementById('ProductSku').value = data.sku;
                    document.getElementById('ProductDescription').value = data.description;
                    setProductVariantPrices(data.variant_prices)
                    setProductVariant(data.variants)
                    setImage(data.url)
                    setUpdatePage(data.id)
                  
                })
                .catch(error => console.log(error));

            // Now you can use the ID variable as needed
        }
    }, []);

    const handleDrop = acceptedFiles => {
        const file = acceptedFiles[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
   
    // handle click event of the Add button
    const handleAddClick = () => {
        let all_variants = JSON.parse(props.variants.replaceAll("'", '"')).map(el => el.id)
        let selected_variants = productVariants.map(el => el.option);
        let available_variants = all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 == entry2))
        setProductVariant([...productVariants, {
            option: available_variants[0],
            tags: []
        }])
    };

    // handle input change on tag input
    const handleInputTagOnChange = (value, index) => {
        let product_variants = [...productVariants]
        product_variants[index].tags = value
        setProductVariant(product_variants)

        checkVariant()
    }

    // remove product variant
    const removeProductVariant = (index) => {
        let product_variants = [...productVariants]
        product_variants.splice(index, 1)
        setProductVariant(product_variants)
    }

    // check the variant and render all the combination
    const checkVariant = () => {
        let tags = [];

        productVariants.filter((item) => {
            tags.push(item.tags)
        })

        setProductVariantPrices([])

        getCombn(tags).forEach(item => {
            setProductVariantPrices(productVariantPrice => [...productVariantPrice, {
                title: item,
                price: 10,
                stock: 10
            }])
        })

    }

    // combination algorithm
    function getCombn(arr, pre) {
        pre = pre || '';
        if (!arr.length) {
            return pre;
        }
        let ans = arr[0].reduce(function (ans, value) {
            return ans.concat(getCombn(arr.slice(1), pre + value + '/'));
        }, []);
        return ans;
    }

    // Save product
    let saveProduct = (event) => {
        event.preventDefault()
        const productName = document.getElementById('ProductName').value;
        const productSku = document.getElementById('ProductSku').value;
        const productDescription = document.getElementById('ProductDescription').value;
        // const imagefile = file[0].name
        const variants = productVariants
        const variantPrices = productVariantPrices

        const formData = new FormData();
        formData.append('image', image);
        formData.append('name', productName);
        formData.append('sku', productSku);
        formData.append('description', productDescription);
        formData.append('variants', JSON.stringify(variants));
        formData.append('variant_prices', JSON.stringify(variantPrices));
        formData.append('productId', updatePage);

        const csrftoken = getCookie('csrftoken');
        fetch('/product/api/list/', {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                //csrf
                'X-CSRFToken':csrftoken
                
            },
            body: formData
        })
        .then(response => {
            document.getElementById('ProductName').value = ""
            document.getElementById('ProductSku').value = ""
            document.getElementById('ProductDescription').value = ""

            setImage(null)
            setProductVariant([
                
            ])
            setProductVariantPrices([])
            setUpdatePage(0)
            window.location.href = '/product/list/'

        })
        .then(data =>{})


        // TODO : write your code here to save the product
    }


    return (
        <div>
            <section>
                <div className="row">
                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div className="card-body">
                                <div className="form-group">
                                    <label htmlFor="">Product Name</label>
                                    <input id='ProductName' type="text" placeholder="Product Name" className="form-control"/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="">Product SKU</label>
                                    <input id='ProductSku' type="text" placeholder="Product Name" className="form-control"/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="">Description</label>
                                    <textarea  id="ProductDescription" cols="30" rows="4" className="form-control"></textarea>
                                </div>
                            </div>
                        </div>

                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Media</h6>
                            </div>
                            <div className="card-body border">
                            <Dropzone onDrop={handleDrop}>
                                {({ getRootProps, getInputProps }) => (
                                    <section>
                                        <div {...getRootProps()}>
                                            <input {...getInputProps()} />
                                            <p>Drag 'n' drop some files here, or click to select files</p>
                                        </div>
                                        {image && <img src={image} alt="Uploaded" style={{ width: 300, height: 300 }} />}
                                    </section>
                                )}
                            </Dropzone>
                            </div>
                        </div>
                    </div>

                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Variants</h6>
                            </div>
                            <div className="card-body">

                                {
                                    productVariants.map((element, index) => {
                                        return (
                                            <div className="row" key={index}>
                                                <div className="col-md-4">
                                                    <div className="form-group">
                                                        <label htmlFor="">Option</label>
                                                        <select className="form-control" defaultValue={element.option}>
                                                            {
                                                                JSON.parse(props.variants.replaceAll("'", '"')).map((variant, index) => {
                                                                    return (<option key={index}
                                                                                    value={variant.id}>{variant.title}</option>)
                                                                })
                                                            }

                                                        </select>
                                                    </div>
                                                </div>

                                                <div className="col-md-8">
                                                    <div className="form-group">
                                                        {
                                                            productVariants.length > 1
                                                                ? <label htmlFor="" className="float-right text-primary"
                                                                         style={{marginTop: "-30px"}}
                                                                         onClick={() => removeProductVariant(index)}>remove</label>
                                                                : ''
                                                        }

                                                        <section style={{marginTop: "30px"}}>
                                                            <TagsInput value={element.tags}
                                                                       style="margin-top:30px"
                                                                       onChange={(value) => handleInputTagOnChange(value, index)}/>
                                                        </section>

                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    })
                                }


                            </div>
                            <div className="card-footer">
                                {productVariants.length !== 3
                                    ? <button className="btn btn-primary" onClick={handleAddClick}>Add another
                                        option</button>
                                    : ''
                                }

                            </div>

                            <div className="card-header text-uppercase">Preview</div>
                            <div className="card-body">
                                <div className="table-responsive">
                                    <table className="table">
                                        <thead>
                                        <tr>
                                            <td>Variant</td>
                                            <td>Price</td>
                                            <td>Stock</td>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {
                                            productVariantPrices.map((productVariantPrice, index) => {
                                                return (
                                                    <tr key={index}>
                                                        <td>{productVariantPrice.title}</td>
                                                        <td><input className="form-control" value={productVariantPrice.price} type="text"/></td>
                                                        <td><input className="form-control" value={productVariantPrice.stock} type="text"/></td>
                                                    </tr>
                                                )
                                            })
                                        }
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button type="button" onClick={saveProduct} className="btn btn-lg btn-primary">Save</button>
                <button type="button" className="btn btn-secondary btn-lg">Cancel</button>
            </section>
        </div>
    );
};

export default CreateProduct;
