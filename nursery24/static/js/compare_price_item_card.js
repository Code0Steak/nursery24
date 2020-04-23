const template3=document.createElement('template')
template3.innerHTML=`
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<style>
        .card {
            display: inline-block;
        }

        .card-img-top {
            width: 100%;
            height: 15vw;
            object-fit: cover;
        }

        .d-block {
            height: 20vw;
            object-fit: cover;
        }

        li {
            list-style-type: none;
        }
    </style>
<div class="card mr-3" style="width: 255px;">
    <img class="card-img-top" id='image' style="{width: 100%,height: 15vw,object-fit: cover;}">

    <div class="card-body">
        <h5 class="card-title"><span id='name'></span></h5>
        <h6 class="card-subtitle text-muted">Rs. <span id='price'></span></h6>
    </div>

    <div class="btn-toolbar ml-1 mb-2" role="toolbar" aria-label="Toolbar with button groups">
        
        <div class="btn-group mr-2" role="group" aria-label="Second group">
            <button type="button" id="compare" class="btn btn-primary">Compare Price</button>
        </div>

        <div class="btn-group mr-2" role="group" aria-label="First group">
            <button type="button" class="btn btn-success" id = "inc">+</button>
            <button type="button" class="btn btn-outline-secondary disabled" id = "result">0</button>
            <button type="button" class="btn btn-success" id = "dec">-</button>
        </div>
    </div>
</div>`
        
class ComparePriceItemCard extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'})
        this.shadowRoot.appendChild(template3.content.cloneNode(true))
        this.shadowRoot.querySelector('h5').innerText=this.getAttribute('name')
        this.shadowRoot.querySelector('#price').innerText=this.getAttribute('price')
        this.shadowRoot.querySelector('#image').src=this.getAttribute('image')
        // this.shadowRoot.querySelector('#direct').addEventListener('click',()=>{
        //     location.href='/consumer/compareprices?id='+this.getAttribute('id')
        // })
        var btn=this.shadowRoot.querySelector('#compare')

        btn.onclick= (event) =>{
            location.href='/consumer/compareprices?id='+this.getAttribute('id')
        }
    }


    connectedCallback(){

        let name = this.shadowRoot.querySelector('h5').innerHTML;
        let price = this.shadowRoot.querySelector('#price').innerHTML;
        let img = this.shadowRoot.querySelector('#image').src;
        //increments product in cookie
        this.shadowRoot.querySelector("#inc").addEventListener('click',()=>{
            
            let decodedCookie = decodeURIComponent(document.cookie).split(';');
        
            //console.log(price,name,decodedCookie);
            if(!decodedCookie.find(item => item.includes("product="))){
                let product = [{name: name, quantity: 1,perPrice: price,price: price,img: img}]
                //console.log(product);
                document.cookie = 'product=' + JSON.stringify(product);
                //console.log(document.cookie);
                this.shadowRoot.querySelector("#result").innerHTML = product[0].quantity;
                
                console.log(product);
            }
            else{
                let productString = decodedCookie.find(item => item.includes("product="));
                //console.log(productString); success
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
               // console.log(product);// success
                if(!product.find(item=> item.name == name)){
                    let newProduct = {name: name,quantity: 1, perPrice: price, price: price, img: img};
                    this.shadowRoot.querySelector("#result").innerHTML = newProduct.quantity;

                    product = [...product,newProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);
                }
                else
                {
                    let thisProduct = product.find(item => item.name == name);
                    product = product.filter(item=> item.name !=name);
                    if(!(thisProduct.providers)){
                                 
                        thisProduct.quantity += 1;
                        thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                        this.shadowRoot.querySelector("#result").innerHTML = thisProduct.quantity;
                        
                    }
                    else{
                        let ye = thisProduct.providers.find(item=> item.perPrice == price);
                        thisProduct.providers = thisProduct.providers.filter(item=> item.perPrice != price)
                        ye.quantity += 1;
                        ye.price = ye.perPrice * ye.quantity;
                        this.shadowRoot.querySelector("#result").innerHTML = thisProduct.providers.reduce((subtotal,item)=>{return item.quantity + subtotal},0);
                        thisProduct.providers = [...thisProduct.providers,ye];
                    }
                    product = [...product,thisProduct];
                    console.log(product);
                    document.cookie = 'product=' + JSON.stringify(product);  
                
                }
            }
        });
            //decrements product in cookie
            this.shadowRoot.querySelector("#dec").addEventListener('click', async ()=>{
                let decodedCookie = decodeURIComponent(document.cookie).split(';');
                if(decodedCookie.find(item => item.includes("product="))){
                let productString = decodedCookie.find(item => item.includes("product="));
                let productStringSplit = productString.split('=');
                let product = JSON.parse(productStringSplit[1]);
                if(product != []){
                    if(product.find(item=> item.name == name)){
                        
                        if(!product.providers){
                            if(product.find(item=> item.name == name).quantity != 0){
                                let thisProduct = product.find(item=> item.name == name);
                        product = product.filter(item=> item.name != name);
                        thisProduct.quantity -= 1;
                        thisProduct.price = thisProduct.perPrice * thisProduct.quantity;
                        this.shadowRoot.querySelector('#result').innerHTML = thisProduct.quantity;
                        if(thisProduct.quantity!= 0){
                            product = [...product,thisProduct];
                        }
                        document.cookie = 'product=' + JSON.stringify(product);
                            }
                        }
                        
                        else{
                            if(thisProduct.providers.find(item=>item.perPrice == price)){
                                let ye = thisProduct.providers.find(item=>item.perPrice==price);
                                thisProduct.providers = thisProduct.providers.filter(item=>item.perPrice != price);
                                ye.quantity -= 1;
                                if(ye.quantity != 0){
                                    ye.price = ye.quantity * ye.perPrice;
                                    thisProduct.providers = [...thisProduct.providers,ye];
                                }
                                this.shadowRoot.querySelector('result').innerHTML = thisProduct.providers.reduce((subtotal,item)=>{return item.quantity + subtotal},0);
                                product = [...product,thisProduct];
                                document.cookie = 'product=' + JSON.stringify(product);
                            }else{
                                location.href='/consumer/compareprices?id='+this.getAttribute('id');
                            }
                        }
                        
                        
                        

                    }
                }
                }
            });
    }
    
}

window.customElements.define('compare-price-item-card',ComparePriceItemCard)
