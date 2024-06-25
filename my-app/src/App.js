import React, {useState, useEffect} from 'react'
import api from './api'

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    men: false,
    age: '',
    height: ''
  });
//この辞書型は、formDataの初期値を設定している。

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions/');
      setTransactions(response.data);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
    }
  };

  
//after randering the component, fetch the transactions
  useEffect(() => {
    fetchTransactions();
  }, []);
//if you take this ', []' out, it will run the fetchTransactions() infinitely, again and again and again....


//checkbox の変更を検知するための関数
  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/transactions/', formData);
    fetchTransactions();
    setFormData({
      name: '',
      men: false,
      age: '',
      height: ''
    });
  };

  return (
    <div>
      <nav className='navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>
            Weight Prediction App
          </a>
        </div>
      </nav>  

      <div className='container'>
        <form onSubmit={handleFormSubmit}>

          <div className='mb-3 mt-3'>
            <label htmlFor='name' className='form-label'>
              name
            </label>
            <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='men' className='form-label'>
              men
            </label>
            <input type='checkbox' id='men' name='men' onChange={handleInputChange} value={formData.men}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='age' className='form-label'>
              age
            </label>
            <input type='text' className='form-control' id='age' name='age' onChange={handleInputChange} value={formData.age}/>
          </div>

          <div className='mb-3'>
            <label htmlFor='height' className='form-label'>
              height
            </label>
            <input type='text' className='form-control' id='height' name='height' onChange={handleInputChange} value={formData.height}/>
          </div>

          <button type='submit' className='btn btn-primary'>
            submit
          </button>
        </form>

        <table className='table table-striped table-bordered table-hover'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Men</th>
            <th>age</th>
            <th>height</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.id}</td>
              <td>{transaction.name}</td>
              <td>{transaction.men ? 'Yes' : 'No'}</td>
              <td>{transaction.age}</td>
              <td>{transaction.height}</td>
            </tr>
          ))}
        </tbody>
        </table>
      </div>
    </div>
  )
  }

export default App;
