const form=document.querySelector(".inputb");
const submit=document.querySelector("#Submit");
const searchbox=document.querySelector("#searchbox");


form.addEventListener("submit",(e)=>{
    e.preventDefault();
    const text=searchbox.value;
    console.log(text);

    const object={
        'key':text};
    console.log(object);
    $.ajax({
        
    })

    
});

