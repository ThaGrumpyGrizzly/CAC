import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut,
  onAuthStateChanged 
} from 'firebase/auth'
import { 
  collection, 
  addDoc, 
  getDocs, 
  deleteDoc, 
  updateDoc, 
  doc, 
  query, 
  where 
} from 'firebase/firestore'
import { auth, db } from '../firebase'

// Authentication functions
export const registerUser = async (email, password, username) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password)
    const user = userCredential.user
    
    // Store additional user data in Firestore
    await addDoc(collection(db, 'users'), {
      uid: user.uid,
      email: email,
      username: username,
      createdAt: new Date()
    })
    
    return user
  } catch (error) {
    throw new Error(error.message)
  }
}

export const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password)
    return userCredential.user
  } catch (error) {
    throw new Error(error.message)
  }
}

export const logoutUser = async () => {
  try {
    await signOut(auth)
  } catch (error) {
    throw new Error(error.message)
  }
}

export const getCurrentUser = () => {
  return auth.currentUser
}

export const onAuthChange = (callback) => {
  return onAuthStateChanged(auth, callback)
}

// Investment/Purchase functions
export const addPurchase = async (purchaseData) => {
  try {
    const user = getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const docRef = await addDoc(collection(db, 'purchases'), {
      ...purchaseData,
      userId: user.uid,
      createdAt: new Date()
    })
    
    return { id: docRef.id, ...purchaseData }
  } catch (error) {
    throw new Error(error.message)
  }
}

export const getPurchases = async () => {
  try {
    const user = getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const q = query(collection(db, 'purchases'), where('userId', '==', user.uid))
    const querySnapshot = await getDocs(q)
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }))
  } catch (error) {
    throw new Error(error.message)
  }
}

export const updatePurchase = async (purchaseId, purchaseData) => {
  try {
    const user = getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    const purchaseRef = doc(db, 'purchases', purchaseId)
    await updateDoc(purchaseRef, {
      ...purchaseData,
      updatedAt: new Date()
    })
    
    return { id: purchaseId, ...purchaseData }
  } catch (error) {
    throw new Error(error.message)
  }
}

export const deletePurchase = async (purchaseId) => {
  try {
    const user = getCurrentUser()
    if (!user) throw new Error('User not authenticated')
    
    await deleteDoc(doc(db, 'purchases', purchaseId))
  } catch (error) {
    throw new Error(error.message)
  }
}

// Stock search function (we'll use a free API)
export const searchStocks = async (query) => {
  try {
    // Using a free stock API
    const response = await fetch(`https://api.polygon.io/v3/reference/tickers?search=${query}&active=true&limit=10&apiKey=YOUR_POLYGON_API_KEY`)
    const data = await response.json()
    
    return data.results?.map(item => ({
      ticker: item.ticker,
      name: item.name,
      type: item.type
    })) || []
  } catch (error) {
    console.error('Stock search error:', error)
    return []
  }
} 