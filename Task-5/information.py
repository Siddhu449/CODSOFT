import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f8f9fa')
        
        # Data file
        self.data_file = "contacts.json"
        self.contacts = self.load_contacts()
        
        # Create GUI
        self.create_widgets()
        self.refresh_contact_list()
        
    def load_contacts(self):
        """Load contacts from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    return json.load(file)
            except:
                return []
        return []
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.data_file, 'w') as file:
            json.dump(self.contacts, file, indent=4)
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📞 Contact Manager",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left frame - Contact form
        left_frame = tk.Frame(main_container, bg='#ffffff', relief='ridge', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        # Contact form
        form_title = tk.Label(
            left_frame,
            text="Contact Details",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        form_title.pack(pady=10)
        
        # Form fields
        form_frame = tk.Frame(left_frame, bg='#ffffff')
        form_frame.pack(padx=20, pady=10, fill='x')
        
        # Name
        tk.Label(form_frame, text="Name *", font=('Arial', 10, 'bold'), 
                bg='#ffffff', fg='#34495e').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Phone
        tk.Label(form_frame, text="Phone *", font=('Arial', 10, 'bold'), 
                bg='#ffffff', fg='#34495e').grid(row=1, column=0, sticky='w', pady=5)
        self.phone_entry = tk.Entry(form_frame, font=('Arial', 11), width=25)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Email
        tk.Label(form_frame, text="Email", font=('Arial', 10, 'bold'), 
                bg='#ffffff', fg='#34495e').grid(row=2, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(form_frame, font=('Arial', 11), width=25)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Address
        tk.Label(form_frame, text="Address", font=('Arial', 10, 'bold'), 
                bg='#ffffff', fg='#34495e').grid(row=3, column=0, sticky='w', pady=5)
        self.address_entry = tk.Text(form_frame, font=('Arial', 11), width=25, height=3)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        
        # Buttons frame
        button_frame = tk.Frame(left_frame, bg='#ffffff')
        button_frame.pack(pady=15)
        
        self.add_btn = tk.Button(
            button_frame,
            text="➕ Add Contact",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            width=12,
            command=self.add_contact
        )
        self.add_btn.grid(row=0, column=0, padx=5)
        
        self.update_btn = tk.Button(
            button_frame,
            text="✏️ Update",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            width=12,
            command=self.update_contact,
            state='disabled'
        )
        self.update_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=('Arial', 11, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=12,
            command=self.clear_form
        )
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Right frame - Contact list and search
        right_frame = tk.Frame(main_container, bg='#ffffff', relief='ridge', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Search frame
        search_frame = tk.Frame(right_frame, bg='#ecf0f1')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="🔍 Search:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1').pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 11), width=25)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        # Contact list
        list_frame = tk.Frame(right_frame, bg='#ffffff')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for contacts
        columns = ('Name', 'Phone', 'Email')
        self.contact_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show='headings',
            height=15
        )
        
        # Define headings
        self.contact_tree.heading('Name', text='Name')
        self.contact_tree.heading('Phone', text='Phone')
        self.contact_tree.heading('Email', text='Email')
        
        # Set column widths
        self.contact_tree.column('Name', width=150)
        self.contact_tree.column('Phone', width=120)
        self.contact_tree.column('Email', width=180)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.contact_tree.yview)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)
        
        self.contact_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection
        self.contact_tree.bind('<<TreeviewSelect>>', self.on_contact_select)
        
        # Delete button
        self.delete_btn = tk.Button(
            right_frame,
            text="🗑️ Delete Contact",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.delete_contact
        )
        self.delete_btn.pack(pady=10)
        
        # Current selected contact index
        self.selected_contact_index = -1
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get('1.0', tk.END).strip()
        
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields!")
            return
        
        # Check if phone already exists
        for contact in self.contacts:
            if contact['phone'] == phone:
                messagebox.showwarning("Duplicate Phone", "A contact with this phone number already exists!")
                return
        
        contact = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        
        self.contacts.append(contact)
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully!")
    
    def update_contact(self):
        """Update selected contact"""
        if self.selected_contact_index == -1:
            messagebox.showwarning("Selection Error", "Please select a contact to update!")
            return
        
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get('1.0', tk.END).strip()
        
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required fields!")
            return
        
        # Check if phone already exists (excluding current contact)
        for i, contact in enumerate(self.contacts):
            if contact['phone'] == phone and i != self.selected_contact_index:
                messagebox.showwarning("Duplicate Phone", "A contact with this phone number already exists!")
                return
        
        # Update contact
        self.contacts[self.selected_contact_index] = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_form()
        self.update_btn.config(state='disabled')
        messagebox.showinfo("Success", "Contact updated successfully!")
    
    def delete_contact(self):
        """Delete selected contact"""
        if self.selected_contact_index == -1:
            messagebox.showwarning("Selection Error", "Please select a contact to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            self.contacts.pop(self.selected_contact_index)
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_form()
            self.update_btn.config(state='disabled')
            messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def search_contacts(self, event=None):
        """Search contacts by name or phone"""
        search_term = self.search_entry.get().lower().strip()
        
        if not search_term:
            self.refresh_contact_list()
            return
        
        filtered_contacts = [
            contact for contact in self.contacts
            if (search_term in contact['name'].lower() or 
                search_term in contact['phone'].lower() or
                search_term in contact.get('email', '').lower())
        ]
        
        self.refresh_contact_list(filtered_contacts)
    
    def on_contact_select(self, event):
        """Handle contact selection from list"""
        selection = self.contact_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        contact_name = self.contact_tree.item(item)['values'][0]
        contact_phone = self.contact_tree.item(item)['values'][1]
        
        # Find the contact index
        for i, contact in enumerate(self.contacts):
            if contact['name'] == contact_name and contact['phone'] == contact_phone:
                self.selected_contact_index = i
                self.populate_form(contact)
                self.update_btn.config(state='normal')
                break
    
    def populate_form(self, contact):
        """Populate form with contact data"""
        self.clear_form()
        self.name_entry.insert(0, contact['name'])
        self.phone_entry.insert(0, contact['phone'])
        self.email_entry.insert(0, contact.get('email', ''))
        self.address_entry.insert('1.0', contact.get('address', ''))
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete('1.0', tk.END)
        self.selected_contact_index = -1
        self.update_btn.config(state='disabled')
    
    def refresh_contact_list(self, contacts=None):
        """Refresh the contact list display"""
        if contacts is None:
            contacts = self.contacts
        
        # Clear existing items
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        # Add contacts to treeview
        for contact in contacts:
            self.contact_tree.insert('', 'end', values=(
                contact['name'],
                contact['phone'],
                contact.get('email', '')
            ))

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()