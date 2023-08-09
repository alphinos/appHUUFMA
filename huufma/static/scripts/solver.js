const submitForm = function( event ){
    if ( event.key === "Enter" ){
        patients.submit()
    }
}

const patients = document.querySelector( "#config" )
patients.addEventListener( "keydown", submitForm )
patients.firstChild.addEventListener( "change", function( event ){

    if ( Number( patients.firstChild.value ) < 0 || isNaN( patients.firstChild.value ) ){
        patients.firstChild.value = 0
    }

    patients.submit()
})

for ( const patient of patients ){
    patient.addEventListener( "change", function(){
        if ( Number( patient.value ) < 0 || isNaN( patient.value ) ){
            patient.value = 0
            return
        }

        patients.submit()
    } )
}

const numberInputs = document.querySelectorAll( "input[type=number]" )
for ( const nInput of numberInputs ){
    nInput.addEventListener( "change", function(){
        if ( Number( nInput.value ) < 0 || isNaN( nInput.value ) ){
            nInput.value = 0
            return
        }
    } )
}

document.addEventListener( "keydown", function( event ){
    if ( event.key === "Enter" ){
        event.preventDefault()
    }
} )