function bisectionForm() {
  return {
    a: '',
    b: '',
    tol: '',
    result: null,
    errorMsg: '',
    async submitForm() {
      console.log("Form submitted", this.a, this.b, this.tol);
      this.result = null;
      this.errorMsg = '';
      try {
        const res = await fetch("http://127.0.0.1:8000/api/bisection", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            a: parseFloat(this.a),
            b: parseFloat(this.b),
            tol: parseFloat(this.tol)
          })
        });

        if (!res.ok) {
          throw new Error("Erreur du serveur");
        }

        this.result = await res.json();
        console.log("API result:", this.result);
      } catch (err) {
        this.errorMsg = "Erreur lors de l'appel à l'API: " + err.message;
        console.error(err);
      }
    }
  }
}

// Make bisectionForm available globally for Alpine.js
window.bisectionForm = bisectionForm;
