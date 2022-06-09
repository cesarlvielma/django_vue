<template>
  <v-container>
    <v-row justify="space-around">
      <v-card width="400">
        <v-card-title>Users</v-card-title>
        <v-table>
          <thead>
            <tr>
              <th class="text-left">
                Full Name
              </th>
              <th class="text-left">
                Address
              </th>
              <th class="text-left">
                Zip Code
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in users"
              :key="user.id"
              >
              <td>{{ user.first_name }} {{ user.last_name }}</td>
              <td>{{ user.address.address_line_1 }}</td>
              <td>{{ user.address.zip_code }}</td>
            </tr>
          </tbody>
        </v-table>
        <v-card-actions class="pt-0">
          <v-btn color="primary" block @click="dialog = true">New User</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      fullscreen
      :scrim="false"
      transition="dialog-bottom-transition">
      <template v-slot:activator="{  }">
      </template>
      <v-card>
        <v-toolbar
          >
          <v-toolbar-title>Create new User</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="dialog = false"
              >
              Close
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.first_name"
                  :rules="stringRules"
                  
                  label="First name"
                  required
                  ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.last_name"
                  :rules="stringRules"
                  
                  label="Last name"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
                >
                <v-select
                  :items="[1,2,3]"
                  label="Customer Rate"
                  v-model="new_user.customer_rate"
                  required
                  >
                </v-select>
              </v-col>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.email"
                  :rules="emailRules"
                  label="E-mail"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.phone"
                  :rules="stringRules"
                  label="Cellphone"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <h2>Address</h2>
            <v-row>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.address.address_line_1"
                  :rules="stringRules"
                  
                  label="Address Line 1"
                  required
                  ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.address.address_line_2"
                  :rules="stringRules"
                  v-on:focusout="callApiGeocoding()"
                  label="Address line 2"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.address.state"
                  :rules="stringRules"
                  v-on:focus="callApiGeocoding()"
                  label="State"
                  required
                  ></v-text-field>
              </v-col>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.address.city"
                  :rules="stringRules"
                  label="City"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="6"
                >
                <v-text-field
                  v-model="new_user.address.zip_code"
                  :rules="stringRules"
                  label="Zip Code"
                  required
                  ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <v-card-actions>
          <v-btn color="primary" block  @click="createUser()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import axios from 'axios'

    export default {
        data() {
            return {
                // users
                users: [],
                dialog: false,
                new_user: {
                  "address": {
                      "id": "14b5aafb-5be3-4158-996c-428035334168",
                      "address_line_1": "2121 7th Ave, Seattle",
                      "address_line_2": "WA 98121, EE. UU.",
                      "state": "",
                      "city": "",
                      "zip_code": "",
                  },
                  "first_name": "Cesar",
                  "last_name": "Vielma",
                  "email": "cesarlvielma@gmail.com",
                  "customer_rate": 1,
                  "phone": "+525581942891",
              },
                valid: false,
                stringRules: [
                  v => !!v || 'Name is required',
                ],
                emailRules: [
                  v => !!v || 'E-mail is required',
                  v => /.+@.+/.test(v) || 'E-mail must be valid',
                ],
            }
        },
        methods: {
            async getData() {
                try {
                    const response = await axios.get('http://localhost:8000/api/users/');
                    this.users = response.data;
                } catch (error) {
                    console.log(error);
                }
            },
          async createUser() {
                try {
                    await axios.post('http://localhost:8000/api/users/', this.new_user);
                    await this.getData();
                    this.dialog = false;
                } catch (error) {
                    console.log(error);
                }
            },
          async callApiGeocoding() {
                try {
                    const response = await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${this.new_user.address.address_line_1},${this.new_user.address.address_line_2}&key=AIzaSyAV_ARybtrN-cW1qnzOcYc7QY6mTY54Cg8`);


                    for (let result of response.data.results[0].address_components){
                      if (result.types.includes('postal_code')) {
                        this.new_user.address.zip_code = result.long_name;
                      }
                      if (result.types.includes('locality') && result.types.includes('political')) {
                        this.new_user.address.city = result.long_name;
                      }

                      if (result.types.includes('administrative_area_level_1') && result.types.includes('political')) {
                        this.new_user.address.state = result.short_name;
                      }


                    }


                } catch (error) {
                    console.log(error);
                }
            },
        },
        created() {
            // Fetch users on page load
            this.getData();
        }
    }
</script>