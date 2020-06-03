print('import navbar')
import dash_bootstrap_components as dbc



def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Faviz", href="/faviz/")),
              dbc.NavItem(dbc.NavLink("Báo cáo tài chính", href="/bctc/")),
              dbc.NavItem(dbc.NavLink("Dupont", href="/dupont/")),
            #   dbc.DropdownMenu(
            #      nav=True,
            #      in_navbar=True,
            #      label="Menu",
            #      children=[
            #         dbc.DropdownMenuItem("Entry 1"),
            #         dbc.DropdownMenuItem("Entry 2"),
            #         dbc.DropdownMenuItem(divider=True),
            #         dbc.DropdownMenuItem("Entry 3"),
            #               ],
            #           ),
                    ],
          brand="Home",
          brand_href="/",
          sticky="top",
        )
     return navbar
