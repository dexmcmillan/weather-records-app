export default (context, inject) => {

    const date = (input_date) => {
        const monthNames = ["Jan.", "Feb.", "March", "April", "May", "June",
            "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."
        ];

        let full_date = new Date(input_date)

        console.log(full_date)
    
        let date = full_date.getDate()
    
        let month = full_date.getMonth()
        month = monthNames[month]
    
        let year = full_date.getFullYear()
        
        return `${month} ${date + 1}, ${year}`
    }
    
    inject('date', date)
  }