//! Implementation of the ``rust:impl::`` directive

use quote::__private::TokenStream;
use quote::{quote, ToTokens};
use syn::{ItemImpl, Visibility};

use crate::directives::{extract_doc_from_attrs, Directive, DirectiveOption, DirectiveVisibility};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

#[derive(Clone, Debug)]
pub(crate) struct ImplDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
    pub(crate) items: Vec<Directive>,
}

impl ImplDirective {
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemImpl,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        let mut name = format!(
            "{}::{}",
            parent_path,
            &item.self_ty.to_token_stream().to_string(),
        );

        let (ig, tg, wc) = item.generics.split_for_impl();
        let ident = item.self_ty.to_token_stream();
        let trait_ = match &item.trait_ {
            Some((bang, path, _)) => {
                let mut trait_name = String::new();
                if bang.is_some() {
                    trait_name += "!";
                }
                trait_name += &*path.segments.last().unwrap().ident.to_string();
                name += "::";
                name += &*trait_name;

                quote! {#path for}
            }
            None => TokenStream::new(),
        };
        let sig = quote! {impl #ig #trait_ #ident #tg #wc};

        let options = vec![
            DirectiveOption::Vis(DirectiveVisibility::Pub),
            DirectiveOption::Sig(sig.to_string()),
            DirectiveOption::Toc(format!(
                "impl {}{}{}",
                trait_,
                if trait_.is_empty() {
                    ""
                }
                else {
                    " "
                },
                ident
            )),
        ];

        let items = Directive::from_impl_items(&name, item.items.iter(), inherited_visibility);
        Directive::Impl(ImplDirective {
            name,
            options,
            content: extract_doc_from_attrs(&item.attrs),
            items,
        })
    }
}

impl RstDirective for ImplDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        let content_indent = Self::make_content_indent(level + 1);

        let mut text = Self::make_rst_header("impl", &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        for item in self.items {
            text.extend(item.get_rst_text(level + 1, max_visibility))
        }

        text
    }
}

impl MdDirective for ImplDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        let fence = Self::make_fence(fence_size);

        let mut text = Self::make_md_header("impl", &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        for item in self.items {
            text.extend(item.get_md_text(fence_size - 1, max_visibility));
        }

        text.push(fence);
        text
    }

    fn fence_size(&self) -> usize {
        Self::calc_fence_size(&self.items)
    }
}
