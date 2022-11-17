export default (context, inject) => {

    const date = (input_date) => {
        const monthNames = ["Jan.", "Feb.", "March", "April", "May", "June",
            "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."
        ];
    
        let date = new Date(input_date).getDate()
    
        let month = new Date(input_date).getMonth()
        month = monthNames[month]
    
        let year = new Date(input_date).getFullYear()
        
        return `${month} ${date}, ${year}`
    }
    
    inject('date', date)
  }